import os
import random
import sys
import xml.etree.ElementTree as ElementTree

import requests
import re

from os import path

def get_namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

def create_out_folder():
    out_folder = ""
    for i in range(1000):
        out_folder = os.getcwd() + '/out/' + str(i)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
            break

    return out_folder


def download_file(bucket_url, url, out_folder):
    file_name = url.rsplit('/', 1)[1]
    print('[+] Download of ' + file_name)
    r = requests.get(bucket_url + '/' + url)

    if path.exists(out_folder + '/' + file_name):
        file_name = str(random.randint(0, 100)) + '_' + file_name

    with open(out_folder + '/' + file_name, 'wb') as f:
        f.write(r.content)


def parse_xml(bucket_list_result, bucket_url, out_folder):
    tree = ElementTree.parse(bucket_list_result)
    root = tree.getroot()
    namespace = get_namespace(root)
    for elem in root:
        for sub_elem in elem:
            if sub_elem.tag == namespace+'Key' and '.' in sub_elem.text:
                download_file(bucket_url, sub_elem.text, out_folder)


def retrieve_bucket_list_result(url, out_folder):
    print('[+] Download bucket list result of ' + url)
    r = requests.get(url)

    with open(out_folder + '/content.xml', 'wb') as f:
        f.write(r.content)


def main():
    if len(sys.argv) >= 2:
        bucket_url = sys.argv[1]
        out_folder = create_out_folder()
        retrieve_bucket_list_result(bucket_url, out_folder)
        parse_xml(out_folder + '/content.xml', bucket_url, out_folder)

    else:
        print('Usage: python download_bucket.py <bucket_url>')


if __name__ == '__main__':
    main()