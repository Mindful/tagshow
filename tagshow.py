import sys
import os
import code
import readline
import rlcompleter
import shutil
import re
from image import Image
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
        dup = (len([img for img in IMAGES if img.path == name]) > 0)
        #"in" operator wasn't doing the job, the above is hacky (should redefine an operator instead) but quick
        if not dup:
            IMAGES.append(Image(name))
        return True
    except Exception as e:
        print("Could not get image with name", name)
        print(e)


def __get_dir():
    files = [name for name in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), name)) and
                "."+name.split(".")[-1] in EXTENSIONS]
    for file in files:
        __get_image(file)

#TODO: we could save the last version and add an undo(), though we'd also have to save the last command so we could undo
#saves by saving the last version
#also we could better display changes like [x] -> [y]

def transcribe_function():
    frame = inspect.currentframe().f_back
    name = inspect.getframeinfo(frame)[2]
    args, _, _, values = inspect.getargvalues(frame)
    global BUILDER
    arglist = []
    for arg in args:
        arglist.append(values[arg])
    BUILDER.record_command(name+str(arglist).replace("[", "(").replace("]", ")"))



#TODO: both get and unget could/should take a variable number of args
def get(name):
    failures = 0
    for extension in EXTENSIONS:
        if __get_image(name+extension):
            __get_image(name+extension)
            success = name+extension
            break
        else:
            failures += 1
            print("Could not find image as "+name+extension)

    if failures == len(EXTENSIONS):
        raise "Could not find image "+name
    else:
        print("Found image as "+success)

    display()


def unget(name):
    for ext in EXTENSIONS:
        exname = name+ext
        for img in IMAGES:
            if img.path == exname:
                del IMAGES[IMAGES.index(img)]

    display()

#Start transcribed functions -------

def where_has_prop(property_name):
    transcribe_function()
    __get_dir()
    global IMAGES
    IMAGES = IMAGES.where_has_prop(property_name)
    display()


def where_prop_equals(property_name, value):
    transcribe_function()
    __get_dir()
    global IMAGES
    IMAGES = IMAGES.where_prop_equals(property_name, value)
    display()


def where_prop_contains(property_name, value):
    transcribe_function()
    __get_dir()
    global IMAGES
    IMAGES = IMAGES.where_prop_contains(property_name, value)
    display()


def where_prop_greater(property_name, value):
    transcribe_function()
    __get_dir()
    global IMAGES
    IMAGES = IMAGES.where_prop_greater(property_name, value)
    display()

def where_prop_lesser(property_name, value):
    transcribe_function()
    __get_dir()
    global IMAGES
    IMAGES = IMAGES.where_prop_lesser(property_name, value)
    display()


def slideshow(show_name, include_scripts = True, include_images = True):
    transcribe_function()
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
    render(show_name)
    os.chdir(prev_directory)
    global BUILDER
    BUILDER.output(show_name, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    BUILDER = ShowBuilder()

#End transcribed functions -------

def get_dir():
    print("Getting dir...")
    __get_dir()
    IMAGES.sort(key=operator.attrgetter('path'))
    display()

def image_by_image():
    print("For tags with values, please use the notation <tag>:<value>. Otherwise, a tag by itself will default to"
          "a value of true.")
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
    files = [name for name in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), name)) and
                "."+name.split(".")[-1] in EXTENSIONS and re.fullmatch(prefix+'\d+', name.split(".")[0])]
    for file in files:
        __get_image(file)
    display()


def display():
    print(IMAGES)


def tag(tagname, value=True):
    for img in IMAGES:
        img[tagname] = value
    display()


def clear_tags():
    for img in IMAGES:
        img.clear()
    display()


def clear():
    global IMAGES
    del IMAGES[:]
    display()

def save():
    for img in IMAGES:
        img.save_properties()
    print(IMAGES, " successfully saved")


def render(show_name):
    for img in IMAGES:
        img.render()
    with open(show_name+'.html', 'w') as f:
        f.write(Canvas.render())
    print("Slideshow named", '"'+show_name+'"', "successfully compiled from ", IMAGES)



def set_script_dir(name):
    if os.path.exists(name):
        global SCRIPT_DIR
        SCRIPT_DIR = name
    else:
        raise "Nonexistant directory"

def set_img_dir(name):
    if os.path.exists(name):
        global IMG_DIR
        IMG_DIR = name
    else:
        raise "Nonexistant directory"
