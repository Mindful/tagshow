from illustrations.fetchers.pixiv_fetcher import PixivFetcher
from illustrations.fetchers.danbooru_fetcher import DanbooruFetcher
from illustrations import index

def test():
    indexx = index.Index.get_or_create_instance()
    indexx.cleanup()
    a = PixivFetcher()
    a.fetch(max_count=5)

    print(indexx.data)


def test_danbooru():
    indexx = index.Index.get_or_create_instance()
    indexx.cleanup()

    a = DanbooruFetcher()
    a.fetch(max_count=5)
    print(indexx.data)



if __name__ =='__main__':
    test_danbooru()