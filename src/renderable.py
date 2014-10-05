import json

class Canvas:

    scripts = ["jquery", "cycle2", "fullscreen", "cycle2.tile", "cycle2.shuffle", "cycle2.scrollVert", "slideshow"]

    images = []

    options = {"stretch_to_fit": True, "change_interval_ms": 4000, "fullscreen_key":'f'}
    #Strecth to fit NYI



    doc = ""

    @staticmethod
    def append(string):
        Canvas.doc += string+"\n"

    @staticmethod
    def render():
        Canvas.doc = ""
        Canvas.append("<!DOCTYPE html>\n<html>")

        #Header
        Canvas.append("<head>")
        Canvas.append("\n".join([('<script type="text/javascript" src="'+script+'.js"></script>') for script in
                                 Canvas.scripts]))
        Canvas.append("</head>")

        #Style
        Canvas.append("<style>")
        Canvas.append("#slideshow { width: 100%; height:100%;} div {background-color: black;} body {background-color: black;}")
        Canvas.append("</style>")

        #Script
        #Slideshow options
        slideshow_options = {"autoHeight": "false",
                             "manualTrump": "false",
                             "fx": "fade",
                             "timeout": Canvas.options["change_interval_ms"]}

        Canvas.append("<script>")
        Canvas.append("$(function(){initSlideShow("+json.dumps(Canvas.options)+","+json.dumps(slideshow_options)+");});")
        Canvas.append("</script>")

        #Body/Slideshow
        Canvas.append('<body>\n<div id="slideshow" data-cycle-auto-height=false>')
        Canvas.append("".join([image.html() for image in Canvas.images]))
        Canvas.append('</div>\n</body>')

        Canvas.append("</html>")
        return Canvas.doc
    


class RenderableImage:
    def __init__(self, path):
        self.path = path

    def render(self):
        Canvas.images.append(self)

    def html(self):
        return '<img src="'+self.path+'">'