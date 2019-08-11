from illustrations.fetchers.pixiv_fetcher import PixivFetcher
from illustrations.fetchers.danbooru_fetcher import DanbooruFetcher
from illustrations import index

def test_pixiv():
    indexx = index.Index.get_or_create_instance()
    indexx.cleanup()
    a = PixivFetcher()
    a.fetch(max_count=5)

    print(indexx.data)


def test_danbooru():
    indexx = index.Index.get_or_create_instance()
    indexx.cleanup()
    print(indexx.get_all_illustrations()[0].get_tags())
    print(indexx.data)

    a = DanbooruFetcher()
    a.fetch(max_count=5)
    print(indexx.data)


def test_all():
    indexx = index.Index.get_or_create_instance()
    indexx.cleanup()
    a = PixivFetcher()
    a.fetch(max_count=5)

    a = DanbooruFetcher()
    a.fetch(max_count=5)
    print(indexx.data)






if __name__ =='__main__':
    test_danbooru()
    #test_pixiv()