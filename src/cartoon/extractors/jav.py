#! -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from cartoon.util import log
from cartoon.common import *

HOST = "https://www.jav468.com/"
SITE_NAME = "_"


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def get_title(content: str) -> str:
    bs = get_bs_element(content)
    return bs.title.string


def get_all_links_for_list(content: str) -> List[str]:
    bs = get_bs_element(content)
    result: List[str] = []
    wrapper = bs.findAll("div", attrs={"class": "thumbnail"})
    for div in wrapper:
        for child in div.children:
            if child.name == "a":
                result.append(child.attrs["href"])
    return result


def get_imgs_from_page(content: str) -> List[str]:
    bs = get_bs_element(content)
    wrapper = bs.find("figure", attrs={"class": "wp-block-image"})
    result: List[str] = []
    for child in wrapper.children:
        if child.name == "img" and "lazyload" in child.attrs["class"]:
            result.append(child.attrs["data-src"])
    return result


def download_list(url: str):
    content: Optional[str] = str(get_content(url), encoding="utf-8")
    if not content:
        return
    all_link = get_all_links_for_list(content)
    for link in all_link:
        download_one(link)
        log.i("downloaded " + link)

    if url.endswith("/"):
        url = str(url[:-1])
    items = url.split("/")
    page = items.pop(-1)
    newUrl = "/".join((items + [str(int(page) + 1)]))
    download_list(newUrl)


def download_one(url: str):
    print(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    images: List[str] = get_imgs_from_page(content)
    folder = get_title(content)
    safe_f = "".join(
        [c for c in folder if c.isalpha() or c.isdigit() or c == " "]
    ).rstrip()
    url_file_tuple: List[Tuple[str, str]] = [
        (img, img.split("/")[-1]) for img in images
    ]
    urls_save(url_file_tuple, safe_f)


prefer_download = download_one
prefer_download_list = download_list
