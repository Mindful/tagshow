import urllib.request
import gzip
import shutil
import os

from PIL import Image

from taggers.base_tagger import BaseTagger


class I2VTagger(BaseTagger):

    SOURCE_NAME = 'illust2vec'

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

    def compute_tags(self, illustration):
        img = Image.open(illustration.location)
        results = self.illust2vec.estimate_plausible_tags([img], threshold=0.5)[0]
        output_tags = [tag_tuple[0] for tag_tuple in results['general']]
        rating = max(results['rating'], key=lambda x: x[1])[0]
        output_tags.append('rating:'+rating)
        output_tags.extend(results['character'])

        return output_tags


