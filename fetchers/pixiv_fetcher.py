from pixivpy3 import *
from urllib.parse import urlparse, parse_qs
from index import Index
import os.path
import yaml


class PixivFetcher:

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
            bookmarks_response = self.api.user_bookmarks_illust(self.user_id, max_bookmark_id=self.next_max_bookmark_id)
            self.illusts_current_page = bookmarks_response['illusts']
            next_page_url = bookmarks_response['next_url']
            if next_page_url is None:
                raise StopIteration
            else:
                query_parameters = parse_qs(urlparse(next_page_url).query)
                self.next_max_bookmark_id = query_parameters['max_bookmark_id']

    def __init__(self):
        self.app_api = AppPixivAPI()
        login_response = self.app_api.login(user, password)
        self.user_id = login_response['response']['user']['id']

    def collect_illustrations(self):
        bookmarks_iterator = self.BookmarksIterator(self.app_api, self.user_id)
        return [illustration for illustration in bookmarks_iterator if illustration is not None][0:5] #TODO: REMOVE THIS LIMIT OF FIVE

    def download_and_register_illustrations(self, illustrations):
        image_registration_arguments = []
        for illustration in illustrations:
            image_url = illustration.meta_single_page.get('original_image_url', illustration.image_urls.large)
            tags = [tag['name'] for tag in illustration.tags]

            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]
            name = 'pixiv_{}{}'.format(str(illustration.id), extension)

            self.app_api.download(url=image_url, name=name)
            image_registration_arguments.append((name, tags))

        Index.get_or_create_instance().register_new_illustration_list(image_registration_arguments)

    def fetch_single_page_bookmarks(self):
        illustrations = self.collect_illustrations()
        single_illustrations = [illustration_data for illustration_data in illustrations
                                if illustration_data['page_count'] == 1]
        multi_illustrations = [illustration_data for illustration_data in illustrations
                               if illustration_data['page_count'] > 1]
        self.download_and_register_illustrations(single_illustrations)






def test():
    a = PixivFetcher()
    b = a.fetch_single_page_bookmarks()
    print(b)

if __name__ =='__main__':
    test()






