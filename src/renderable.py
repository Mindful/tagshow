class Canvas:

    html = "<!DOCTYPE html><html>"

    images = []

    options = {"stretch_images": True} #This option NYI, and more options to come later
    


class RenderableImage:
    def __init__(self, path):
        self.path = path

    def render(self):
        Canvas.images.append(self)