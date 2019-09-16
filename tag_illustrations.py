from taggers import i2v_tagger
from illustrations.index import Index
import sys


def main():
    index = Index.get_or_create_instance()
    index.cleanup()

    tagger_name = sys.argv[1].lower()
    if tagger_name == 'i2v':
        tagger = i2v_tagger.I2VTagger()
        tagger.add_tags_to_illustrations(index.get_all_illustrations())
    elif tagger_name == 'danbooru':
        raise Exception("Danbooru tagger not yet implemented")
    elif tagger_name == 'all':
        tagger = i2v_tagger.I2VTagger()
        tagger.add_tags_to_illustrations(index.get_all_illustrations())
        raise Exception("Danbooru tagger not yet implemented")
    else:
        raise Exception("Unknown fetcher name - please try \"i2v\", \"danbooru\", or \"all\"")

if __name__ =='__main__':
    main()