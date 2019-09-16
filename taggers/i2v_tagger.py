import urllib.request
import gzip
import shutil
import os

from PIL import Image

from common.named_logger import NamedLogger


class I2VTagger(NamedLogger):


    models_downloaded = False

    model_file_list = ['https://github.com/rezoo/illustration2vec/releases/download/v2.0.0/tag_list.json.gz',
                  'https://github.com/rezoo/illustration2vec/releases/download/v2.0.0/illust2vec_tag.prototxt',
                  'https://github.com/rezoo/illustration2vec/releases/download/v2.0.0/illust2vec_tag_ver200.caffemodel',
                  'https://github.com/rezoo/illustration2vec/releases/download/v2.0.0/illust2vec_ver200.caffemodel']

    def __init__(self):
        self.missing_model_files = [url for url in self.model_file_list if not os.path.exists(os.path.split(url)[1])]

        if len(self.missing_model_files) == 0:
            self.log("Model files already downloaded")
        else:
            self.log("Downloading models...")
            self.download_models()
            self.log("Download complete")

        import i2v
        self.illust2vec = i2v.make_i2v_with_chainer("illust2vec_tag_ver200.caffemodel", "tag_list.json")

    def download_models(self):
        for file in self.missing_model_files:
            self.log("Downloading ", file)
            urllib.request.urlretrieve(file, os.path.split(file)[1])

        with gzip.open('tag_list.json.gz', 'rb') as f_in:
            with open('tag_list.json', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def image_tags(self, image):
        img = Image.open(image)
        return self.illust2vec.estimate_plausible_tags([img], threshold=0.5)


