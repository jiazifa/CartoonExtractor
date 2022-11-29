#! -*- coding: utf-8 -*-

import os
import typing
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from cartoon.util import log
from cartoon.common import *

HOST = "www.177pic.info/"
SITE_NAME = "_"

CONFIG_FILE_NAME: str = ".ct_config_downloaded"

PicItem = typing.NamedTuple(
    "PicItem",
    [("url", str), ("page_url", str), ("folder", str), ("path", str)]
)

if not os.path.exists(CONFIG_FILE_NAME):
    with open(CONFIG_FILE_NAME, mode='w') as file:
        file.writelines(["\n"])


def write_done_urls(url: str):
    with open(CONFIG_FILE_NAME, mode='a+') as file:
        file.writelines(["\n", url])


def is_downloaded(url: str) -> bool:
    urls: set = {}
    with open(CONFIG_FILE_NAME, mode="r") as file:
        urls = set(file.readlines())
    return url in urls


def get_random_num(digit: int = 6) -> str:
    """ get a random num
    
    get random num 
    Args:
        digit: digit of the random num, limit (1, 32)
    Return:
        return Generated random num
    """
    if digit is None:
        digit = 1
    digit = min(max(digit, 1), 32)    # 最大支持32位
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


def get_all_links_for_list(content: str) -> typing.List[str]:
    """
    获得本页所有的链接(一个链接就是一本漫画)，通常这个链接的集合表示的是一部漫画
    """
    bs = get_bs_element(content)
    result: List[str] = []

    wrapper = bs.findAll("article")
    for div in wrapper:
        for child in div.descendants:
            if child.name != "a":
                continue
            if 'rel' not in child.attrs:
                continue
            result.append(child.attrs["href"])
    return list(set(result))


def get_imgs_from_page(content: str) -> typing.List[str]:
    """
    获得每页中所有的漫画页面链接
    """
    bs = get_bs_element(content)
    wrapper = bs.find("div", attrs={"class": "single-content"})
    result: List[str] = []
    if wrapper:
        for child in wrapper.descendants:
            if child.name == "img":
                if "data-lazy-src" in child.attrs:
                    src = child.attrs["data-lazy-src"]
                else:
                    src = child.attrs["src"]
                result.append(src)
    return result


def get_pages_url_by_first_page_content(
    content: str
) -> typing.Iterable[str]:    # 通过下载地址判断一共有多少页
    bs = get_bs_element(content)
    result: List[str] = []
    page = bs.find(attrs={'class': 'page-links'})    # 直接查找attrs判断页面
    if page:
        for child in page.descendants:
            if child.name != "a":
                continue
            if 'href' not in child.attrs:
                continue
            result.append(child.attrs["href"])
    return sorted(result)


def _get_images_by_wright(folder: str, url: str) -> typing.List[PicItem]:
    """通过浏览器打开，获取本页中所有的图片链接，这个是备用方法，消耗资源较大，尽量不要使用

    Args:
        folder (str): 下载到文件夹
        url (str): 页面的地址，这就是解析的目标网页

    Returns:
        typing.List[PicItem]: 解析网页中所有的图片
    """
    with sync_playwright() as pw:
        browser = pw.webkit.launch(
            headless=False, proxy={"server": "http://127.0.0.1:7890"}
        )
        page = browser.new_page()
        page.goto(url, timeout=20000)
        browser.close()
        return []


def get_all_images_from_one_page(folder: str,
                                 url: str) -> typing.List[PicItem]:
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")

    images: List[str] = get_imgs_from_page(content)
    # 数量太多了就明显不是了，直接跳过
    if len(images) > 300:
        return []
    items = [
        PicItem(img, \
            url, \
            folder, \
            os.path.join(folder, img.split("/")[-1])
        )
        for img in images
    ]
    if not all([item.url.startswith("http") for item in items]):
        items = _get_images_by_wright(folder, url)
    return items


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
    download_list(newUrl)


def download_one(url: str):
    log.i(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    title = get_title(content)
    if is_downloaded(url=url):
        return
    all_pages_ = get_pages_url_by_first_page_content(content)

    folder = title
    safe_f = "".join(
        [c for c in folder if c.isalpha() or c.isdigit() or c == " "]
    ).rstrip()
    temp_f = f".{safe_f}"
    all_pages_.append(url)
    all_images: typing.List[PicItem] = []
    for page in all_pages_:
        images_in_one_page = get_all_images_from_one_page(temp_f, page)
        all_images.extend(images_in_one_page)

    if not all_images:
        return
    if not all([str(item.url).startswith("http") for item in all_images]):
        return
    log.i(f"收集 {title} 链接完成，正在进行下载")

    if not os.path.exists(temp_f):
        os.mkdir(temp_f)

    pool = ThreadPoolExecutor(max_workers=10)
    for item in all_images:
        pool.submit(url_save, item.url, item.path)

    pool.shutdown(True)
    log.i(f"下载完成,正在转储...")
    # 如果
    if os.path.exists(temp_f):
        os.rename(temp_f, safe_f)

    write_done_urls(url)


def safe_one(url: str):
    try:
        download_one(url)
    except Exception as e:
        log.i(f"{e}")


prefer_download = safe_one
prefer_download_list = download_list

if __name__ == "__main__":
    # prefer_download('http://www.177picyy.com/html/2022/11/5284010.html')
    prefer_download_list('http://www.177picyy.com/html/category/tt/')