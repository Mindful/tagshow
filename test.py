from taggers import i2v_tagger
from illustrations.index import Index


def main():
    i = Index.get_or_create_instance()
    img = i.get_all_illustrations()[0]
    a = i2v_tagger.I2VTagger()
    print(a.image_tags(img.location))

if __name__ == '__main__':
    main()