from illustrations.fetchers.base_fetcher import BaseFetcher
from illustrations.index import Index
import urllib
from illustrations.illustration_download import IllustrationDownload
from illustrations.fetchers.fetcher_exception import FetcherException
from pybooru import Danbooru

class DanbooruFetcher(BaseFetcher):

    SOURCE_NAME = 'danbooru'
    RATING_MAP = {'e':'explicit', 'q':'questionable', 's':'safe'}

    class TagQueryIterator:

        def __init__(self, client, tags):
            self.client = client
            self.tags = tags
            self.page = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.page == 0:
                self._next_posts_page()
            try:
                return self.posts_current_page.pop()
            except IndexError:
                self._next_posts_page()

        def _next_posts_page(self):
            self.page += 1
            self.posts_current_page = self.client.post_list(tags=self.tags, limit=50, page=self.page)
            if len(self.posts_current_page) == 0:
                raise StopIteration

    def __init__(self):
        self.index = Index.get_or_create_instance()
        config = self.get_config()[DanbooruFetcher.SOURCE_NAME]

        conf_login = config['login']
        conf_api_key = config['api_key']
        self.username = conf_login
        self.client = Danbooru('danbooru', username=conf_login, api_key=conf_api_key)

        exclude_ratings = config['exclude_ratings']
        for rating in exclude_ratings:
            if rating not in DanbooruFetcher.RATING_MAP.keys():
                raise FetcherException("Unrecognized rating to be excluded (must be \"e\", \"q\", or \"s\"")

        if len(exclude_ratings) == 3:
            raise FetcherException("No images will be fetched if all three ratings are excluded")

        self.exclude_ratings = exclude_ratings

    def _collect_bookmarked_posts(self):
            return list(self.TagQueryIterator(self.client, self._compute_search_string()))

    def _compute_search_string(self):
        search_string = 'fav:{}'.format(self.username)
        for rating in self.exclude_ratings:
            search_string = search_string + ' -rating:{}'.format(rating)

        return search_string

    def _compute_download_targets(self, bookmarked_posts):
        download_targets = []
        for post in bookmarked_posts:
            tag_list = post['tag_string_general'].split(' ')
            tag_list.append('rating:{}'.format(DanbooruFetcher.RATING_MAP[post['rating']]))
            extension = self.file_extension_from_image_url(post['file_url'])

            target = IllustrationDownload(DanbooruFetcher.SOURCE_NAME, post['id'], post['file_url'], extension, tags=tag_list)
            download_targets.append(target)

        return download_targets

    def _download_and_register(self, download_targets):
        completed_downloads = []
        for target in download_targets:
            self.log("Downloading ", target)

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Python Tagshow')] #Danbooru blocks default urllib user agent
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(target.url, target.name)

            completed_downloads.append(target)

        self.index.register_new_illustration_list(completed_downloads)

    def fetch(self, max_count=None):
        existing_ids = self.index.present_ids_for_source(DanbooruFetcher.SOURCE_NAME)
        bookmarked_posts = self._collect_bookmarked_posts()
        if max_count:
            bookmarked_posts = bookmarked_posts[0:max_count]

        self.log("Found ", len(existing_ids), " posts already present from the same source")
        unprocessed_posts = [post for post in bookmarked_posts if post['id'] not in existing_ids]
        self.log(len(unprocessed_posts), " posts to be downloaded")

        download_targets = self._compute_download_targets(unprocessed_posts)
        self._download_and_register(download_targets)