import re
from bs4 import BeautifulSoup
from cartoon.common import *
import requests

IMAGE_HOST = "https://i3.mmzztt.com/"
HOST = "https://www.mzitu.com/"
SITE_NAME = "妹子图"


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def all_albums(content: str) -> List[str]:
    result: List[str] = []
    bs = get_bs_element(content)
    wrapper = bs.findAll("ul", attrs={"class": "archives"})
    for w in wrapper:
        for child in w.descendants:
            if child.name == "a":
                src = child.attrs["href"]
                result.append(src)
    return result


def get_title(content: str) -> str:
    bs = get_bs_element(content)
    keepcharacters = (" ", ".", "_")
    return "".join(
        c for c in bs.title.string if c.isalnum() or c in keepcharacters
    ).rstrip()


def get_image_url(content: str) -> List[str]:
    result: List[str] = []
    bs = get_bs_element(content)
    wrapper = bs.find("div", attrs={"class": "main-image"})
    for child in wrapper.descendants:
        if child.name == "img":
            result.append(child.attrs["src"])
    return result


def get_next_page_link(current: str, content: str) -> Optional[str]:
    bs = get_bs_element(content)
    a_s = bs.find_all("a")

    a = list(filter(lambda tag: tag.string and "下一页" in tag.string, a_s))
    if not a:
        return None
    return a[0]["href"]


def download_one(url: str):
    content: Optional[str] = str(
        requests.get(url, headers=FAKE_HEADER).content, encoding="utf-8"
    )
    all_links: List[str] = []
    folder = get_title(content or "")
    while content:
        links = get_image_url(content)
        all_links.extend(links)
        next_page = get_next_page_link(url, content)
        if not next_page:
            content = None
        else:
            url = next_page
            content = str(
                requests.get(url, headers=FAKE_HEADER).content, encoding="utf-8"
            )
    safe_f = "".join(
        [c for c in folder if c.isalpha() or c.isdigit() or c == " "]
    ).rstrip()
    url_file_tuple: List[Tuple[str, str]] = [
        (img, img.split("/")[-1]) for img in all_links
    ]
    urls_save(url_file_tuple, safe_f)


def download_list(url: str):
    url = "https://www.mzitu.com/all/"
    content: str = str(requests.get(url, headers=FAKE_HEADER).content, encoding="utf-8")
    pages = all_albums(content)
    pages = list(set(pages))
    for p in pages:
        download_one(p)


prefer_download = download_one
prefer_download_list = download_list
