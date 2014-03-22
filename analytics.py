#!/usr/bin/env python
import json
import exifread
import os, fnmatch
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file, __version__


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


def parse_gps(titude):
    first_number = titude.split(',')[0]
    second_number = titude.split(',')[1]
    third_number = titude.split(',')[2]
    third_number_parent = third_number.split('/')[0]
    third_number_child = third_number.split('/')[1]
    third_number_result = float(third_number_parent) / float(third_number_child)
    return float(first_number) + float(second_number)/60 + third_number_result/3600


jsonFile = open("gps.geojson", "w")
jsonFile.writelines('{\n"type": "FeatureCollection","features": [\n')


def write_data(paths):
    index = 1
    for path in all_files('./' + paths, '*.jpg'):
        f = open(path[2:], 'rb')
        tags = exifread.process_file(f)
        # jsonFile.writelines('"type": "Feature","properties": {"cartodb_id":"'+str(index)+'"},"geometry": {"type": "Point","coordinates": [')
        latitude = tags['GPS GPSLatitude'].printable[1:-1]
        longitude = tags['GPS GPSLongitude'].printable[1:-1]
        # print tags['GPS GPSLongitudeRef']
        # print tags['GPS GPSLatitudeRef']
        jsonFile.writelines('{"type": "Feature","properties": {"cartodb_id":"' + str(index) + '"')
        # jsonFile.writelines(',"OS":"' + str(tags['Image Software']) + '","Model":"' + str(tags['Image Model']) + '","Picture":"'+str(path[7:])+'"')
        jsonFile.writelines('},"geometry": {"type": "Point","coordinates": [' + str(parse_gps(longitude)) + ',' + str(
            parse_gps(latitude)) + ']}},\n')
        index += 1


write_data('imgs')

jsonFile.writelines(']}\n')
jsonFile.close()