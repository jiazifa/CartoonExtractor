#! -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from cartoon.common import *

HOST = "https://www.jav468.com/"
SITE_NAME = "_"


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs

def get_title(content: str) -> str:
    bs = get_bs_element(content)
    return bs.title.string

def get_imgs_from_page(content: str) -> List[str]:
    bs = get_bs_element(content)
    wrapper = bs.find("figure", attrs={"class": "wp-block-image"})
    result: List[str] = []
    for child in wrapper.children:
        if child.name == "img" and "lazyload" in child.attrs["class"]:
            result.append(child.attrs["data-src"])
    return result


def download_list(url: str):
    pass


def download_one(url: str):
    print(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    images: List[str] = get_imgs_from_page(content)
    folder = get_title(content)
    safe_f = "".join([c for c in folder if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    url_file_tuple: List[Tuple[str, str]] = [(img, img.split("/")[-1]) for img in images]
    urls_save(url_file_tuple, safe_f)

prefer_download = download_one
prefer_download_list = download_list