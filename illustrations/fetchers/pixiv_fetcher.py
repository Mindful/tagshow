import os.path
from urllib.parse import urlparse, parse_qs
from pixivpy3 import *
from illustrations.fetchers.base_fetcher import BaseFetcher
from illustrations.index import Index
from illustrations.illustration_download import IllustrationDownload


class PixivFetcher(BaseFetcher):

    SOURCE_NAME = 'pixiv'

    class BookmarksIterator:
        def __init__(self, pixiv_api, user_id):
            self.api = pixiv_api
            self.user_id = user_id
            self.next_max_bookmark_id = None

        def __iter__(self):
            return self

        def __next__(self):
            if self.next_max_bookmark_id is None:
                self._next_bookmark_page()
            try:
                return self.illusts_current_page.pop()
            except IndexError:
                self._next_bookmark_page()

        def _next_bookmark_page(self):
            bookmarks_response = self._get_user_bookmark_illusts_eng(self.user_id, self.next_max_bookmark_id)
            self.illusts_current_page = bookmarks_response['illusts']
            next_page_url = bookmarks_response['next_url']
            if next_page_url is None:
                raise StopIteration
            else:
                query_parameters = parse_qs(urlparse(next_page_url).query)
                self.next_max_bookmark_id = query_parameters['max_bookmark_id']

        def _get_user_bookmark_illusts_eng(self, user_id, max_bookmark_id):
            #TODO: we'd rather just use api.user_bookmarks_illust but can't, see https://github.com/upbit/pixivpy/issues/76
            url = 'https://app-api.pixiv.net/v1/user/bookmarks/illust'
            params = {
                'user_id': user_id,
                'restrict': 'public',
                'filter': 'for_ios',
                'max_bookmark_id': max_bookmark_id
            }
            r = self.api.no_auth_requests_call('GET', url, params=params, req_auth=True,
                                               headers={'Accept-Language':'en-US'})
            return self.api.parse_result(r)

    def __init__(self):
        self.app_api = AppPixivAPI()
        config = self.get_config()['pixiv']

        conf_login = config['login']
        conf_password = config['password']
        self.log("Attempting to log in as ", conf_login)
        login_response = self.app_api.login(conf_login, conf_password)
        self.user_id = str(login_response['response']['user']['id'])

    def _collect_bookmarked_illustrations(self):
        self.log("Fetching list of bookmarks for user id ", self.user_id)
        bookmarks_iterator = self.BookmarksIterator(self.app_api, self.user_id)
        bookmarked_illustrations = [illustration for illustration in bookmarks_iterator if illustration is not None][
        0:5]  # TODO: REMOVE THIS LIMIT OF FIVE

        self.log("Found ", len(bookmarked_illustrations), " bookmarked illustrations")
        return bookmarked_illustrations

    def _compute_download_targets(self, illustrations):
        download_targets = []
        for illustration in illustrations:
            tags = [tag['translated_name'] if tag['translated_name'] else tag['name'] for tag in illustration.tags]

            if illustration['page_count'] > 1:
                for meta_page in illustration.meta_pages:
                    print("SKIPPING META PAGE")
                    # image_url = meta_page['image_urls']['large']
                    # target = self._construct_download_target(image_url, illustration.id, tags)
                    # download_targets.append(target)

            else:
                image_url = illustration.meta_single_page.get('original_image_url', illustration.image_urls.large)
                target = self._construct_download_target(image_url, illustration.id, tags)
                download_targets.append(target)

        return download_targets

    def _construct_download_target(self, url, illust_id, tags, page_number=None):
        url_basename = os.path.basename(url)
        extension = os.path.splitext(url_basename)[1][1:]

        if page_number:
            name = 'pixiv_{}_p{}{}'.format(str(illust_id), page_number, extension)
            download_target = IllustrationDownload(PixivFetcher.SOURCE_NAME, illust_id, url, extension, tags,
                                                           metadata={'page':page_number}, name=name)
        else:
            download_target = IllustrationDownload(PixivFetcher.SOURCE_NAME, illust_id, url, extension, tags)

        return download_target

    def _download_and_register(self, download_targets):
        completed_downloads = []
        for target in download_targets:
            self.app_api.download(url=target.url, name=target.name)
            completed_downloads.append(target)

        Index.get_or_create_instance().register_new_illustration_list(completed_downloads)



    def fetch(self):
        bookmarked_illustrations = self._collect_bookmarked_illustrations()
        download_targets = self._compute_download_targets(bookmarked_illustrations)
        self._download_and_register(download_targets)






