#! -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from cartoon.common import *

HOST = "https://www.jav468.com/"
SITE_NAME = "_"


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def get_imgs_from_page(content: str) -> List[str]:
    bs = get_bs_element(content)
    wrapper = bs.find("figure", attrs={"class": "wp-block-image"})
    result: List[str] = []
    for child in wrapper.children:
        if child.name == "img" and "lazyload" in child.attrs["class"]:
            result.append(child.attrs["data-src"])
    return result


def prefer_download_list(url: str):
    pass


def prefer_download(url: str):
    print(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    images: List[str] = get_imgs_from_page(content)
    for img in images:
        url_save(images)
