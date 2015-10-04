from libxmp import XMPFiles, consts, XMPError, XMPMeta
import json


class TaggableImageList(list):

    def where(self, property_name, check):
        return TaggableImageList([img for img in self if (check(img[property_name]))])

    def where_has_prop(self, property_name):
        return TaggableImageList([img for img in self if property_name in img])

    def where_without_prop(self, property_name):
        return TaggableImageList([img for img in self if property_name not in img])

    def where_prop_equals(self, property_name, value):
        return self.where_has_prop(property_name).where(property_name, lambda x: value == x)

    def where_prop_contains(self, property_name, value):
        return self.where_has_prop(property_name).where(property_name, lambda x: self.__safe_contains(value, x))

    def where_prop_greater(self, property_name, value):
        return self.where_has_prop(property_name).where(property_name, lambda x: self.__safe_lesser(value, x))

    def where_prop_lesser(self, property_name, value):
        return self.where_has_prop(property_name).where(property_name, lambda x: self.__safe_greater(value,x))

    def __safe_greater(self, lhs, rhs):
        try:
            return lhs > rhs
        except:
            return False

    def __safe_lesser(self, lhs, rhs):
        try:
            return lhs < rhs
        except:
            return False

    def __safe_contains(self, lhs, rhs):
        try:
            return lhs in rhs
        except:
            return False


class TaggableImage(dict):

    loaded = TaggableImageList()

    xmp_key = "SlideshowProperties"

    def __init__(self, path):
        self.path = path
        self.load_properties()
        TaggableImage.loaded.append(self)

    def __del__(self):
        if self in TaggableImage.loaded:
            TaggableImage.loaded.remove(self)

    def __str__(self):
        return "("+self.path+":"+dict.__str__(self)+")"

    def __repr__(self):
        return "("+self.path+":"+dict.__repr__(self)+")"

    def load_properties(self):
        xmp_file = XMPFiles(file_path=self.path, open_forupdate=False)
        try:
            xmp = xmp_file.get_xmp()
            if xmp is not None:
                prop_list = xmp_file.get_xmp().get_property(consts.XMP_NS_DC, TaggableImage.xmp_key)
            else:
                prop_list = "[]"
        except XMPError:
            return
        prop_list = json.loads(prop_list)
        for key in prop_list:
            self[key] = prop_list[key]
        xmp_file.close_file()

    def save_properties(self):
        xmp_file = XMPFiles(file_path=self.path, open_forupdate=True)
        xmp = xmp_file.get_xmp()
        if xmp is None:
            xmp = XMPMeta()

        xmp.set_property(consts.XMP_NS_DC, TaggableImage.xmp_key, json.dumps(self))
        if xmp_file.can_put_xmp(xmp):
            xmp_file.put_xmp(xmp)
            xmp_file.close_file()
        else:
            raise "Could not write settings to XMP file"

    def xmp(self):
        xmp_file = XMPFiles(file_path=self.path, open_forupdate=False)
        ret = xmp_file.get_xmp()
        xmp_file.close_file()
        return ret

