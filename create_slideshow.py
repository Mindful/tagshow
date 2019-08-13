#!/usr/bin/python

import sys
from slideshow import Slideshow


def main():
    slideshow_name = sys.argv[1]
    slideshow = Slideshow(slideshow_name)
    slideshow.write_slideshow()

if __name__ == "__main__":
    main()



