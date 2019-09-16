TagShow
--

TagShow is a simple set of Python scripts intended primarily to help manage
downloading illustrations from various places (currentl Danbooru and Pixiv)
and compile them into slideshows. 

Dependencies
-- 

The requirements.txt file includes all of the Python dependencies, but
TagShow also requires [jQuery](https://jquery.com/) and
[Galleria](https://galleria.io/) to be present in the `rendering_resources`
directory. 

Usage
--
1. Update the `fetcher_config.yaml` with account information for Pixiv
or Danbooru, and change any other settings you'd like. 
2. Run 
`fetch_illustrations.py` with `pixiv`, `danbooru` or `all` as an argument
to fetch the favorited/bookmarked illustrations on the given account. 
3. Create a `.txt` file with a valid
[yaql](https://yaql.readthedocs.io/en/latest/getting_started.html)  query 
selecting the images you'd like as part of your slideshow. There are two
examples included to help you get started. 
4. Run `create_slideshow.py` with your yaql query text file as an argument. The output will be a directory including a html file you can open to view
the actual slideshow. 

Taggers
--
If you'd like to increase the number of tags available on your images, you can
use the included taggers. These can be run via `tag_illustrations.py` with 
`i2v`, `danbooru` or `all` as an argument. 

The `danbooru` tagger works out of the box, and will search Danbooru for
any images you have downloaded from Pixiv and then update those images with the 
Danbooru tags. In sort, this tagger will add Danbooru tags to your Pixiv images. 

The `i2v_tagger` is slightly more complicated. It uses [Illustration2Vec](https://github.com/rezoo/illustration2vec)
to assign tags to any images you have downloaded and indexed through TagShow, but
it has some dependencies.
1. It requires all of the Illustration2Vec dependencies. It's generally safe to just
use their [requirements.txt](https://github.com/rezoo/illustration2vec/blob/master/requirements.txt) file.
2. It requires that the [i2v](https://github.com/rezoo/illustration2vec/tree/master/i2v) directory
from Illustration2Vec be copied to the top level directory in TagShow.

Dependency Directory Structure
--

If all the dependencies are confusing, here is an abridged version of what
a TagShow directory with the rendering and Illustration2Vec dependencies in 
it might look like:
```
tagshow
├── common
│   ├── ...
│   └── named_logger.py
├── create_slideshow.py
├── fetch_illustrations.py
├── i2v
│   ├── ...
│   └── chainer_i2v.py
├── illustrations
│   ├── ...
│   └── index.py
├── readme.md
├── rendering
│   ├── ...
│   └── slideshow.py
├── rendering_resources
│   ├── galleria-1.5.7
│   │   ├── ...
│   │   ├── package.json
│   │   └── src
│   │       ├── galleria.js
│   │       ├── ...
│   ├── jquery-3.4.1.min.js
│   └── slideshow_template.html
├── requirements.txt
├── slideshow_example_1.txt
├── slideshow_example_2.txt
├── tag_illustrations.py
└── taggers
    ├── ...
    └── i2v_tagger.py

```

Note that the exact versions of jQuery and Galleria are not important; TagShow
will look for their name as a substring. 