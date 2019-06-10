from illustrations.fetchers.pixiv_fetcher import PixivFetcher
from illustrations import index

def test():
    indexx = index.Index.get_or_create_instance()
    indexx.cleanup()
    a = PixivFetcher()
    b = a.fetch()

    print(indexx.data)


if __name__ =='__main__':
    test()