#!/usr/bin/env python

import fnmatch
import os

from PIL import Image


size = 512, 512


def all_files(root, patterns='*', single_level=False, yield_folders=False):
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
                if single_level:
                    break


def resize(picture_path):
    for path in all_files(os.path.expanduser(picture_path), '*.jpg'):
        filename = os.path.splitext(path)[0].rsplit('/', 1)[-1]
        outfile = filename + ".thumbnail.jpg"
        try:
            im = Image.open(path)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save('resize/{0}'.format(outfile), "JPEG")
        except IOError:
            print "cannot create thumbnail for '%s'" % outfile

if __name__ == "__main__":
    resize('~/Pictures/Nokia')