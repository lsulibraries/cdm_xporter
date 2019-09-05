import os
from lxml import etree as ET
import json
import sys


def check(folder):
    for root, dirs, files in os.walk(''):
        xml_files = [i for i in files if '.xml' in i]
        for file in xml_files:
            xml_parsed = ET.parse('{}/{}'.format(root, file)).getroot()
            if xml_parsed.tag == 'error':
                print('{}/{}'.format(root, file))

        json_files = [i for i in files if '.json' in i]
        for file in json_files:
            with open('{}/{}'.format(root, file), 'r') as f:
                parsed_json = json.loads(f.read())
            if 'message' in parsed_json and parsed_json['message'] == "Requested item not found":
                print('{}/{}'.format(root, file))


if __name__ == '__main__':
    try:
        folder = sys.argv[1]
    except IndexError:
        print('\nChange to: "python looking_for_404_records.py $folder\n\n')
        quit()
    check(folder)
