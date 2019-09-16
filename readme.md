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