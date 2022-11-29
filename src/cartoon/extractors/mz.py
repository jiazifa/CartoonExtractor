import re
from bs4 import BeautifulSoup
from cartoon.util import log
from cartoon.common import *

HOST = "http://meizi.info/"
SITE_NAME = "_"


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def get_title(content: str) -> str:
    bs = get_bs_element(content)
    return bs.title.string


def get_images_from_page(content: str) -> List[str]:
    result: List[str] = []
    bs = get_bs_element(content)
    wrapper = bs.findAll("article", attrs={"class": "article-content"})
    for div in wrapper:
        for child in div.descendants:
            if child.name == "img":
                result.append(child.attrs["src"])
    return result


def download_list(url: str):
    pass


def download_one(url: str):
    print(url)
    content: str = str(get_content(url), encoding="utf-8")
    images: List[str] = get_images_from_page(content)
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

if __name__ == "__main__":
    url = "http://meizi.info/htm-data-7-1902-3441888.html"
    download_one(url)