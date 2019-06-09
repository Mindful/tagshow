from illustrations.fetchers.pixiv_fetcher import PixivFetcher

def test():
    a = PixivFetcher()
    b = a.fetch_single_page_bookmarks()
    print(b)

if __name__ =='__main__':
    test()