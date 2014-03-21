#!/usr/bin/env python
import json
import exifread

f = open('Windows Phone_20131201_21_52_17_Pro.jpg', 'rb')

tags = exifread.process_file(f)

print tags['GPS GPSLatitude']
print tags['GPS GPSLongitude']