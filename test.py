from illustrations.fetchers.pixiv_fetcher import PixivFetcher
from illustrations import index

def test():
    a = PixivFetcher()
    b = a.fetch()

    print(index.Index.get_or_create_instance().data)


if __name__ =='__main__':
    test()