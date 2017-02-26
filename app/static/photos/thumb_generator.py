# !/usr/bin/env python

import os, sys, PIL
from PIL import Image, ImageOps

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    size = (300, 300)
    num_generated = 0
    print 'processing...'
    for item in os.listdir(dir_path):
        if item.endswith('.jpg') and not item.startswith('small-'):
            filename = os.path.join(dir_path, item)
            try:
                image = Image.open(filename)
                thumb = ImageOps.fit(image, size, Image.ANTIALIAS)
                thumb.save(os.path.join(dir_path, 'small-' + item), "JPEG")
                num_generated += 1
            except IOError:
                print("cannot create thumbnail for", item)
    print 'generated ' + str(num_generated) + ' thumbnail images.'

if __name__ == '__main__':
    main()
