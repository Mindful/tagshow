import sys
import os
import code
import readline
import rlcompleter
import shutil
import re
from image_old import Image
from renderable import Canvas
from taggable import TaggableImageList
import operator
import inspect
from showbuilder import ShowBuilder

EXTENSIONS = [".jpg", ".png", ".gif"]
IMAGES = TaggableImageList()
BUILDER = ShowBuilder()

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
IMG_DIR = os.getcwd()


def __get_image(name):
    try:
        IMAGES.append(Image(name))
    except Exception as e:
        print("Could not get image with name", name)
        print(e)

def __image_is_dup(name):
    #"in" operator wasn't doing the job, the above is hacky (should redefine an operator instead) but quick
    return (len([img for img in IMAGES if img.path == name]) > 0)


def __get_dir():
    files = [name for name in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), name)) and
                "."+name.split(".")[-1] in EXTENSIONS]
    for file in files:
        __get_image(file)
    IMAGES.sort(key=operator.attrgetter('path'))



def __render(show_name):
    for img in IMAGES:
        img.render()
    with open(show_name+'.html', 'w') as f:
        f.write(Canvas.render())
    print("Slideshow named", '"'+show_name+'"', "successfully compiled from ", IMAGES)

def __auto_get_dir_if_fresh():
    global IMAGES
    if len(IMAGES) == 0:
        print("No images selected, defaulting to selecting from directory")
        __get_dir()

#TODO: we could save the last version and add an undo(), though we'd also have to save the last command so we could undo
#saves by saving the last version
#also we could better display changes like [x] -> [y]

def __transcribe_function():
    frame = inspect.currentframe().f_back
    name = inspect.getframeinfo(frame)[2]
    args, _, _, values = inspect.getargvalues(frame)
    global BUILDER
    arglist = []
    for arg in args:
        arglist.append(values[arg])
    BUILDER.record_command(name+str(arglist).replace("[", "(").replace("]", ")"))



def get(*files):
    """Takes a variable number of files and searches for them in the current directory with all extensions supported by
    the program. If all files are found, they will be added to the current list of images. Otherwise, an exception is
    thrown."""
    file_additions = []
    for filename in files:
        failures = 0
        for extension in EXTENSIONS:
            name_with_extension = filename+extension
            if not __image_is_dup(name_with_extension):
                success = name_with_extension
                file_additions.append(success)
                break
            else:
                failures += 1
                print("Could not find image in directory as "+filename+extension)

        if failures == len(EXTENSIONS):
            raise "Could not find image "+filename
        else:
            print("Found image as "+success)

    for filename in file_additions:
        __get_image(filename)
        print("Getting "+filename)

    display()


def unget(*files):
    """Takes a variable number of files and searches for them in the current list of images with all the extensions
    supported by the program. If all the files are found, they will be removed from the current list of images.
    Otherwise, an exception is thrown"""
    file_removals = []
    for filename in files:
        failures = 0
        for ext in EXTENSIONS:
            name_with_extension = filename+ext
            for img in IMAGES:
                if img.path == name_with_extension:
                    success = name_with_extension
                    file_removals.append(success)
                else:
                    failures += 1
                    print("Could not find image in image list as "+name_with_extension)

        if failures == len(EXTENSIONS):
            raise "Could not find image "+filename
        else:
            print("Found image as "+success)

    for img_file in file_removals:
        del IMAGES[IMAGES.index(img_file)]
        print("Removing "+img_file+" from image list")

    display()

#Start transcribed functions -------

def where_has_tag(tag_name):
    """Selects all images with the given tag from the current list of images, removing images without this tag from
    the list. If the current list of images is empty, instead selects from the current directory."""
    __transcribe_function()
    __auto_get_dir_if_fresh()
    global IMAGES
    IMAGES = IMAGES.where_has_prop(tag_name)
    display()


def where_tag_equals(tag_name, value):
    """Removes all images where the value of the given tag is not equal to the given input value. Images without the tag
     are ignored, and remain in the current list of images. If the current list of images is empty, the directory will be
     loaded before performing the operation."""
    __transcribe_function()
    __auto_get_dir_if_fresh()
    global IMAGES
    IMAGES = IMAGES.where_prop_equals(tag_name, value)
    display()


def where_tag_contains(tag_name, value):
    """Removes all images where the value of the given tag does not contain the given input value according to python's
    "in" operator"). Images without the tag are ignored, and remain in the current list of images. If the current list
    of images is empty, the directory will be loaded before performing the operation."""
    __transcribe_function()
    __auto_get_dir_if_fresh()
    global IMAGES
    IMAGES = IMAGES.where_prop_contains(tag_name, value)
    display()


def where_tag_greater(tag_name, value):
    """Removes all images where the value of the given tag is not less than or equal to the given input value. Images
    without the tag are ignored, and remain in the current list of images. If the current list of images is empty, the
    directory will be loaded before performing the operation."""
    __transcribe_function()
    __auto_get_dir_if_fresh()
    global IMAGES
    IMAGES = IMAGES.where_prop_greater(tag_name, value)
    display()

def where_tag_lesser(tag_name, value):
    """Removes all images where the value of the given tag is not greater than or equal to the given input value. Images
    without the tag are ignored, and remain in the current list of images. If the current list of images is empty, the
    directory will be loaded before performing the operation."""
    __transcribe_function()
    __auto_get_dir_if_fresh()
    global IMAGES
    IMAGES = IMAGES.where_prop_lesser(tag_name, value)
    display()


def slideshow(show_name, include_scripts = True, include_images = True):
    """Compiles a slideshow from all the images in the current list of images using the show_name input value. The
    include_scripts and include_images arguments determine whether or not images and javascript files should be
    included in the slideshow directory, respectively. This is recommended, though not necessary as the HTML files
    just need the files to be accessible somehow. The actual slideshow is an HTML file, and the program will also
    attempt to compile a script that can be used to regenerate a slideshow with the same tags."""
    __transcribe_function()
    if not os.path.exists(show_name):
        os.mkdir(show_name)
    else:
        raise show_name+" already exists as either a file or directory"

    for script in Canvas.scripts:
        shutil.copy(os.path.join(SCRIPT_DIR, script+".js"), os.path.join(show_name, script+".js"))

    for img in IMAGES:
        shutil.copy(os.path.join(IMG_DIR, img.path), os.path.join(show_name, img.path))

    prev_directory = os.getcwd()
    os.chdir(show_name)
    __render(show_name)
    os.chdir(prev_directory)
    global BUILDER
    BUILDER.output(show_name, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    BUILDER = ShowBuilder()

#End transcribed functions -------

def get_dir():
    """Loads every eligible image (as determined by file extensions) in the current directory into the current list
    of images. Note that in some instances this method can take a little while to return."""
    print("Getting dir...")
    __get_dir()
    display()

def image_by_image():
    """Iterates over ever every image in the current list of images, allowing them to be tagged individually. Tags can be
    assigned as CSVs with the notation <tag>:<value>, or tags by themself which will default to a value of "True". Note
    that the <tag> is assumed to be a string and can be unquoted, but <value> must be a valid python value. Raw numbers
    are fine, but strings must be in quotes. Additionally, note that images processed by this method are saved one by
    one as they are processed."""
    print("For tags with values, please use the notation <tag>:<value>. Otherwise, a tag by itself will default to"
          " a value of True. Note that the <tag> is assumed to be a string and can be unquoted, but <value> must be a valid"
          " python value. Raw numbers are fine, but strings must be in quotes.")
    for img in IMAGES:
        a = input("Please enter tags for image \""+img.path+"\" separted by spaces: ")
        tags = a.split(" ")
        for tag in tags:
            if ":" in tag:
                img[tag.split(":")[0]] = eval(tag.split(":")[1])
            else:
                img[tag] = True
        img.save_properties()
        print(img)
    print("Processed all images in directory")



def get_numbered_prefix(prefix):
    """Loads every eligible image (as determined by file extensions) with names constituted by the input value
    immediately followed by a digit into the current list of images. I.E., for an input of "test", this function
    would load files with names "test1", "test2", etc. through "testN"."""
    files = [name for name in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), name)) and
                "."+name.split(".")[-1] in EXTENSIONS and re.fullmatch(prefix+'\d+', name.split(".")[0])]
    for file in files:
        __get_image(file)
    display()


def display():
    """Prints the current list of images."""
    print(IMAGES)


def tag(tag_name, value=True):
    """Adds the given tag name as a tag with the given value. If no value for the tag is passed in, it will default to
     "True" to simply indicate the presence of the tag. Changes not final until saved."""
    for img in IMAGES:
        img[tag_name] = value
    display()


def clear_tags():
    """Clears all tags from all images in the current list of images. Changes not final until saved."""
    for img in IMAGES:
        img.clear()
    display()


def clear():
    """Empties the list of current images. Any unsaved changes to tags will be lost."""
    global IMAGES
    del IMAGES[:]
    BUILDER.clear_commands()
    display()

def save():
    """Saves the list of current images to the disk, writing any changes to the images' tags and making them permanent.
    Note that in some instances this method can take a little while to return."""
    for img in IMAGES:
        img.save_properties()
    print(IMAGES, " successfully saved")

#I don't think there's a viable usecase for the two below methods

# def set_script_dir(name):
#     """Sets the directory from which .js scripts are pulled when compiling slideshows to the input value."""
#     if os.path.exists(name):
#         global SCRIPT_DIR
#         SCRIPT_DIR = name
#     else:
#         raise "Nonexistant directory"

# def set_img_dir(name):
#     """Sets the directory from which image files are pulled when compiling slideshows to the input value."""
#     if os.path.exists(name):
#         global IMG_DIR
#         IMG_DIR = name
#     else:
#         raise "Nonexistant directory"
