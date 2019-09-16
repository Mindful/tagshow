#!/usr/bin/python

import sys

from rendering.slideshow import Slideshow
from illustrations.index import Index



def main():
    index = Index.get_or_create_instance()
    index.cleanup()

    slideshow_name = sys.argv[1]
    slideshow = Slideshow(slideshow_name)
    slideshow.write_slideshow()

if __name__ == "__main__":
    main()



