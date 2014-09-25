class Canvas:

    scripts = ["jquery", "cycle2", "fullscreen", "cycle2.tile", "cycle2.shuffle", "cycle2.scrollVert"]

    images = []

    options = {"stretch_to_fit": True, "change_interval_ms": 4000}
    #Strecth to fit NYI




    @staticmethod
    def render():
        doc = "<!DOCTYPE html><html>"

        #Header
        doc += "<head>"
        doc += "".join([('<script type="test/javascript" src="'+script+'.js"></script>') for script in Canvas.scripts])
        doc += "</head>"

        #Style
        doc += "<style>"
        doc += "#slideshow { width: 100%; height:100%;} div {background-color: black;} body {background-color: black;}"
        doc += "</style>"

        #Script
        #Slideshow options
        slideshow_options = {"autoHeight": "false",
                             "manualTrump": "false",
                             "fx": "fade",
                             "timeout": Canvas.options["change_interval_ms"]}

        doc += "<script>"

        doc += "</script>"

        #Body/Slideshow
        doc += '<body><div id="slideshow" data-cycle-auto-height=false>'
        doc += "".join([image.html for image in Canvas.images])
        doc += '</div></body>'


        doc += "</html>"
    


class RenderableImage:
    def __init__(self, path):
        self.path = path

    def render(self):
        Canvas.images.append(self)

    def html(self):
        return '<img src="'+self.path+'">'