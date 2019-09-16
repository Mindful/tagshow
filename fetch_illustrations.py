from illustrations.fetchers.pixiv_fetcher import PixivFetcher
from illustrations.fetchers.danbooru_fetcher import DanbooruFetcher
from illustrations.index import Index
import sys


def main():
    index = Index.get_or_create_instance()
    index.cleanup()

    fetcher_name = sys.argv[1].lower()
    if fetcher_name == 'pixiv':
        PixivFetcher().fetch()
    elif fetcher_name == 'danbooru':
        DanbooruFetcher().fetch()
    elif fetcher_name == 'all':
        PixivFetcher().fetch()
        DanbooruFetcher().fetch()
    else:
        raise Exception("Unknown fetcher name - please try \"pixiv\", \"danbooru\", or \"all\"")

if __name__ =='__main__':
    main()

