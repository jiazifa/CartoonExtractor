
import re
import codecs
from bs4 import BeautifulSoup
from urllib.parse import urlparse, ParseResult, urlencode, unquote
from cartoon.common import *

HOST = "https://m.kuaikanmanhua.com/"
SITE_NAME = "快看漫画"

IMAGES_REGEX = r'comicImages:(\[[^]]+\])'
URL_REGEX = r'url:\"(.*?)\"'

def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs

def get_imgs_from_page(content: str) -> List[str]:
    c = re.compile(IMAGES_REGEX)
    dict_str = c.findall(content)[0] # 图片的字典信息
    new_c = re.compile(URL_REGEX)
    urls = new_c.findall(dict_str)
    result: List[str] = []
    for u in urls:
        result.append(codecs.decode(u, 'unicode-escape'))
    return result


def get_title(content: str) -> str:
    bs = get_bs_element(content)
    return bs.title.string

def download_all(url: str):
    pass


def download_one(url: str):
    print(url)
    content: Optional[str] = None
    content = str(get_content(url), encoding="utf-8")
    images: List[str] = get_imgs_from_page(content)
    url_names: List[Tuple[str, str]] = []
    dir_name = get_title(content)
    for index, img in enumerate(images):
        u: ParseResult = urlparse(img)
        fn = u.path.split("/")[-1]
        ext = fn.split(".")[-1]
        name = "第{idx}页.{ext}".format(idx=index, ext=ext)
        url_names.append((img, name))
    urls_save(url_names, dir_name)



prefer_download = download_one
prefer_download_list = download_all