A project for tagging images using XMP and spitting them out as simple HTML slideshows. Written primarily for
my own use, and because I was curious about XMP.

TODO:
 - Change the "where_tag_lesser" method not to drop images without that tag from the list.

Dependencies:
 - [jquery](http://jquery.com/)
 - [cycle2](http://jquery.malsup.com/cycle2/)
 - [jquery fullscreen](http://plugins.jquery.com/fullscreen/)
 - [xdotool](http://www.semicomplete.com/projects/xdotool/) (f you want to run the bash script)
 - ...and of course, Python
 
Known Bugs:
 - When using image_by_image(), <key>:<value> pair tags record the value as the first element of a tuple in cases
 where they are not the last tag in the comma-separated list.