#! -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from cartoon.common import *

IMAGE_HOST = "http://p3.manhuapan.com/"
HOST = "https://manhua.fzdm.com/"
SITE_NAME = "风之动漫"


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def get_next_page_link(current: str, content: str) -> Optional[str]:

    bs = get_bs_element(content)
    a_s = bs.find_all("a", "pure-button-primary")

    a = list(filter(lambda tag: tag.string == "下一页", a_s))
    if not a:
        return None
    node = a[0]
    if node.string == "下一页":
        path_spl = current.split("?")[0].split("/")
        path_spl.pop(-1)
        appended: str = node["href"]
        path_spl.append(appended)
        r = "/".join(path_spl)
        return r
    return None


def get_image_name(content: str) -> Optional[str]:
    bs = get_bs_element(content)
    a = bs.find("a", attrs={"class": "button-success"})
    return a.string


def get_target_img_url(content: str) -> Optional[str]:
    pattern = r'var mhurl="([\w\/.]+)'
    result = match1(content, (pattern)) or []
    target = result[0]
    if not target:
        return None
    return IMAGE_HOST + target


def get_title(content: str) -> str:
    bs = get_bs_element(content)
    title: str = bs.title.get_text()
    title = title.replace(SITE_NAME, "").strip()
    return title


def get_filename(img_url: str, title: str, filename: str) -> str:
    return filename + "." + img_url.split(".")[-1]


def prefer_download_list(url: str):
    pass


def prefer_download(url: str):
    print(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    while content:
        target_url = get_target_img_url(content)
        title = get_title(content)
        filename = get_image_name(content)
        if target_url and filename:
            target_filename = get_filename(target_url, title, filename)
            url_save(
                target_url, target_filename,
            )
        next_page = get_next_page_link(url, content)
        if not next_page:
            content = None
        else:
            url = next_page
            content = str(get_content(next_page), encoding="utf-8")
