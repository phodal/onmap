#!/usr/bin/env python

import os
import fnmatch
import exifread


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


def parse_gps(gps):
    first_number = gps.split(',')[0]
    second_number = gps.split(',')[1]
    third_number = gps.split(',')[2]
    third_number_parent = third_number.split('/')[0]
    third_number_child = third_number.split('/')[1]
    third_number_result = float(third_number_parent) / float(third_number_child)
    return float(first_number) + float(second_number) / 60 + third_number_result / 3600


def write_data(file, paths):
    index = 1
    for path in all_files('./' + paths, '*.jpg'):
        f = open(path[2:], 'rb')
        tags = exifread.process_file(f)
        if 'GPS GPSLatitude' in tags:
            latitude = tags['GPS GPSLatitude'].printable[1:-1]
            longitude = tags['GPS GPSLongitude'].printable[1:-1]
            file.writelines('{"type": "Feature","properties": {"cartodb_id":"' + str(index) + '"')
            file.writelines(',"OS":"' + str(tags['Image Software']) + '","Model":"' + str(tags['Image Model']) + '","Picture":"'+str(path[7:])+'"')
            file.writelines('},"geometry": {"type": "Point","coordinates": [' + str(parse_gps(longitude)) + ',' + str(
                parse_gps(latitude)) + ']}},\n')
            index += 1

if __name__ == "__main__":
    
    jsonFile = open("gps.geojson", "w")
    jsonFile.writelines('{\n"type": "FeatureCollection","features": [\n')

    write_data(jsonFile, 'imgs')

    jsonFile.writelines(']}\n')
    jsonFile.close()