from taggable import *

if __name__ == "__main__":
    t1 = TaggableImage("../images/1.jpg")
    t2 = TaggableImage("../images/2.jpg")
    t3 = TaggableImage("../images/3.jpg")

    t1["sketchyness"] = 1
    t2["sketchyness"] = 2
    t3["sketchyness"] = 3

    t1.save_properties()
    t2.save_properties()
    t3.save_properties()

    print(TaggableImage.loaded.where_prop_greater("sketchyness", 1))
