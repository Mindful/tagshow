import os.path
from urllib.parse import urlparse, parse_qs
from pixivpy3 import *
from illustrations.fetchers.base_fetcher import BaseFetcher
from illustrations.index import Index
from illustrations.illustration_download import IllustrationDownload


class PixivFetcher(BaseFetcher):

    SOURCE_NAME = 'pixiv'

    MULTIPAGE_INDIVIDUAL = 'individual'
    MULTIPAGE_ALL = 'all'
    MULTIPAGE_NONE = 'skip'

    MULTIPAGE_VALUES = [MULTIPAGE_INDIVIDUAL, MULTIPAGE_NONE, MULTIPAGE_ALL]

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
        self.index = Index.get_or_create_instance()
        self.app_api = AppPixivAPI()
        config = self.get_config()['pixiv']

        conf_login = config['login']
        conf_password = config['password']
        self.log("Attempting to log in as ", conf_login)
        login_response = self.app_api.login(conf_login, conf_password)
        self.user_id = str(login_response['response']['user']['id'])

        self.multipage_processing = config['process_multipage_illustrations']
        if self.multipage_processing not in PixivFetcher.MULTIPAGE_VALUES:
            raise Exception("Bad config value for pixiv multipage proessing: "+self.multipage_processing)

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
                for page_tuple in self._compute_acceptable_pages_for_illust(illustration):
                    image_url = page_tuple[0]['image_urls']['original']
                    page_number = page_tuple[1]
                    target = self._construct_download_target(image_url, illustration.id, tags, page_number)
                    download_targets.append(target)

            else:
                image_url = illustration.meta_single_page.get('original_image_url', illustration.image_urls.large)
                target = self._construct_download_target(image_url, illustration.id, tags)
                download_targets.append(target)

        return download_targets

    def _pixiv_manual_inspection_url(self, illustration):
        return 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}'.format(illustration.id)

    def _compute_acceptable_pages_for_illust(self, illustration):
        self.log("The illustration at ", self._pixiv_manual_inspection_url(illustration), " has ",
                 len(illustration.meta_pages), " pages")
        if self.multipage_processing == PixivFetcher.MULTIPAGE_ALL:
            self.log("In according with the yaml config, all ", len(illustration.meta_pages),
                     " pages will be downloaded")
            return [(page, index) for index, page in enumerate(illustration.meta_pages, start=1)]
        elif self.multipage_processing == PixivFetcher.MULTIPAGE_NONE:
            self.log("In according with the yaml config, none of these pages will be downloaded")
            return []
        else:
            bad_page_numbers = True
            self.log("Please list the page numbers you would like to download, separated by commas: ")
            while bad_page_numbers:
                page_number_string = input()
                try:
                    result = []
                    page_numbers = [int(num.strip()) for num in page_number_string.split(',')]
                    for num in page_numbers:
                        result.append((illustration.meta_pages[num-1], num))
                    self.log("These pages will be downloaded for illustration ", illustration.id, ": ", page_numbers)
                    return result

                except Exception as e:
                    self.log_warn("Could not process these page numbers due to ", e)
                    self.log("Please enter a single integer, or sequence of integers separated by commas like \"1,2,3\"")

    def _construct_download_target(self, url, illust_id, tags, page_number=None):
        url_basename = os.path.basename(url)
        extension = os.path.splitext(url_basename)[1][1:]

        if page_number:
            name = 'pixiv_{}_p{}.{}'.format(str(illust_id), page_number, extension)
            download_target = IllustrationDownload(PixivFetcher.SOURCE_NAME, illust_id, url, extension, tags,
                                                           metadata={'page':page_number}, name=name)
        else:
            download_target = IllustrationDownload(PixivFetcher.SOURCE_NAME, illust_id, url, extension, tags)

        return download_target

    def _download_and_register(self, download_targets):
        completed_downloads = []
        for target in download_targets:
            self.log("Downloading ", target)
            self.app_api.download(url=target.url, name=target.name)
            completed_downloads.append(target)

        self.index.register_new_illustration_list(completed_downloads)



    def fetch(self):
        existing_ids = self.index.present_ids_for_source(PixivFetcher.SOURCE_NAME)
        bookmarked_illustrations = self._collect_bookmarked_illustrations()

        self.log("Found ", len(existing_ids), " illustrations already present from the same source")

        unprocessed_illustrations = [illustration for illustration in bookmarked_illustrations if illustration.id
                                     not in existing_ids]

        self.log(len(unprocessed_illustrations), " illustrations to be downloaded")



        download_targets = self._compute_download_targets(unprocessed_illustrations)
        self._download_and_register(download_targets)






