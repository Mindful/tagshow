import os
import shutil


class DisplayWriter:

    rendering_resources_foler = 'rendering_resources'
    image_locator_string = 'images go here'

    @staticmethod
    def find_resource(resource_name):
        try:
            return next((x for x in os.listdir("rendering_resources") if resource_name in x))
        except StopIteration:
            raise Exception("Unable to find "+resource_name+" in resources directory")

    def __init__(self, illustration_name_list):
        self.illustration_name_list = illustration_name_list

        jquery_file = self.find_resource('jquery')
        galleria_folder = self.find_resource('galleria')

        self.jquery_loc = os.path.join(DisplayWriter.rendering_resources_foler, jquery_file)
        self.galleria_loc = os.path.join(DisplayWriter.rendering_resources_foler, galleria_folder, 'src', 'galleria.js')
        self.galleria_theme_loc = os.path.join(DisplayWriter.rendering_resources_foler, galleria_folder, 'src', 'themes', 'classic')
        self.html_template = os.path.join(DisplayWriter.rendering_resources_foler, 'slideshow_template.html')


    def write(self, target_folder):
        shutil.copyfile(self.jquery_loc, os.path.join(target_folder, 'jquery.js'))
        shutil.copyfile(self.galleria_loc, os.path.join(target_folder, 'galleria.js'))
        shutil.copytree(self.galleria_theme_loc, os.path.join(target_folder, 'galleria_classic_theme'))

        slideshow_lines = ['          <img src = "' + illustration_name + '">\n' for
                           illustration_name in self.illustration_name_list]

        with open(self.html_template, 'r') as template_file:
            template_lines = template_file.readlines()

        insertion_line = next(i for i,v in enumerate(template_lines) if DisplayWriter.image_locator_string in v) + 1
        output_lines = template_lines[0:insertion_line] + slideshow_lines + template_lines[insertion_line:len(template_lines)]

        with open(os.path.join(target_folder, 'slideshow.html'), 'w') as output_file:
            output_file.writelines(output_lines)




