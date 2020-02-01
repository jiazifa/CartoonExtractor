#! -*- coding: utf-8 -*-
from cartoon.common import *

def prefer_download_list(url):
    pass

def prefer_download(url):
    print(url)
    resp = get_content(url)
    print(resp)
    pass