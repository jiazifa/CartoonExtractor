#! -*- coding: utf-8 -*-

import os
import shutil
from bs4 import BeautifulSoup
from cartoon.util import log
from cartoon.common import *

HOST = "www.177pic.info/"
SITE_NAME = "_"

CONFIG_FILE_NAME: str = ".ct_config_done"

if not os.path.exists(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, mode='w') as file:
            file.writelines(["downloaded"])

def write_done_urls(url: str):
    with open(CONFIG_FILE_NAME, mode='a+') as file:
        file.writelines([url])

def is_downloaded(url: str) -> bool:
    urls: set = {}
    with open(CONFIG_FILE_NAME, mode="r") as file:
        urls = set(file.readlines())
    return url in urls

def get_random_num(digit: int=6) -> str:
    """ get a random num
    
    get random num 
    Args:
        digit: digit of the random num, limit (1, 32)
    Return:
        return Generated random num
    """
    if digit is None:
        digit = 1
    digit = min(max(digit, 1), 32)  # 最大支持32位
    result = ""
    while len(result) < digit:
        append = str(random.randint(1, 9))
        result = result + append
    return result

def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def get_title(content: str) -> str:
    bs = get_bs_element(content)
    return bs.title.string


def get_all_links_for_list(content: str) -> List[str]:
    """
    获得本页所有的链接，通常这个链接的集合表示的是一部漫画
    """
    bs = get_bs_element(content)
    result: List[str] = []

    wrapper = bs.findAll("article")
    for div in wrapper:
        for child in div.descendants:
            if child.name != "a" :
                continue
            if 'rel' not in child.attrs:
                continue
            result.append(child.attrs["href"])
    return result


def get_imgs_from_page(content: str) -> List[str]:
    """
    获得每页中所有的漫画页面链接
    """
    bs = get_bs_element(content)
    wrapper = bs.find("div", attrs={"class": "single-content"})
    result: List[str] = []
    if wrapper:
        for child in wrapper.descendants:
            if child.name == "img": 
                result.append(child.attrs["src"])
    return result


def get_pages_url_by_first_page_content(content: str):    # 通过下载地址判断一共有多少页
    bs = get_bs_element(content)
    result: List[str] = []
    page = bs.find(attrs={'class':'page-links'}) # 直接查找attrs判断页面
    if page:
        for child in page.descendants:
            if child.name != "a" :
                continue
            if 'href' not in child.attrs:
                continue
            result.append(child.attrs["href"])
    return sorted(result)

def just_download_one_images(url: str) -> str:
    """ 仅仅下载一个页面中的所有图片 """
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    
    images: List[str] = get_imgs_from_page(content)
    if len(images) > 300:
        return
    folder = get_title(content)
    safe_f = "".join(
        [c for c in folder if c.isalpha() or c.isdigit() or c == " "]
    ).rstrip()
    url_file_tuple: List[Tuple[str, str]] = [
        (img, img.split("/")[-1]) for img in images
    ]
    urls_save(url_file_tuple, safe_f)
    write_done_urls(url)
    return safe_f

def download_list(url: str):
    content: Optional[str] = str(get_content(url), encoding="utf-8")
    if not content:
        return
    all_link = get_all_links_for_list(content)

    for link in all_link:
        safe_one(link)
        log.i("downloaded " + link)

    if url.endswith("/"):
        url = str(url[:-1])
    items = url.split("/")
    page = items.pop(-1)
    newUrl = "/".join((items + [str(int(page) + 1)]))
    log.i("prepare to parse " + newUrl)
    download_list(newUrl)


def download_one(url: str):
    log.i(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    title = get_title(content)
    # if os.path.exists(title):
    #     return
    all_pages_ = get_pages_url_by_first_page_content(content)
    all_pages_.append(url)
    all_folders = []
    for page in all_pages_:
        if is_downloaded(page):
            continue
        f_name = just_download_one_images(page)
        all_folders.append(f_name)
    log.i("合并{}".format(title))
    return
    # 合并文件夹
    target_folder = title
    try: os.mkdir(target_folder)
    except: ...
    for folder in all_folders:
        for name in os.listdir(folder):
            if os.path.exists(folder):
                source_path = os.path.join(folder, name)
                target_path = os.path.join(target_folder, name)
                try:
                    shutil.move(source_path, target_path)
                except:
                    ...
        shutil.rmtree(folder)
    
def safe_one(url: str):
    try:
        download_one(url)
    except:
        ...

prefer_download = safe_one
prefer_download_list = download_list
