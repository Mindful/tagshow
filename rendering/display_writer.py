import os
import shutil

class DisplayWriter:

    rendering_resources_foler = 'rendering_resources'

    jquery_file = 'jquery-3.4.1.min.js'
    galleria_folder = 'galleria-1.5.7'

    jquery_loc = os.path.join(rendering_resources_foler, jquery_file)
    galleria_loc = os.path.join(rendering_resources_foler, galleria_folder, 'src', 'galleria.js')
    galleria_theme_loc = os.path.join(rendering_resources_foler, galleria_folder, 'src', 'themes', 'classic')
    html_template = os.path.join(rendering_resources_foler, 'slideshow_template.html')

    image_locator_string = 'images go here'



    def __init__(self, illustration_name_list):
        self.illustration_name_list = illustration_name_list


    def write(self, target_folder):
        shutil.copyfile(DisplayWriter.jquery_loc, os.path.join(target_folder, 'jquery.js'))
        shutil.copyfile(DisplayWriter.galleria_loc, os.path.join(target_folder, 'galleria.js'))
        shutil.copytree(DisplayWriter.galleria_theme_loc, os.path.join(target_folder, 'galleria_classic_theme'))

        slideshow_lines = ['          <img src = "' + illustration_name + '">\n' for
                           illustration_name in self.illustration_name_list]

        with open(DisplayWriter.html_template, 'r') as template_file:
            template_lines = template_file.readlines()

        insertion_line = next(i for i,v in enumerate(template_lines) if DisplayWriter.image_locator_string in v) + 1
        output_lines = template_lines[0:insertion_line] + slideshow_lines + template_lines[insertion_line:len(template_lines)]

        with open(os.path.join(target_folder, 'slideshow.html'), 'w') as output_file:
            output_file.writelines(output_lines)




