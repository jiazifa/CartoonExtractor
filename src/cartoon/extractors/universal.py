#! -*- coding: utf-8 -*-

__all__ = ['universal_download']

from ..common import *
from bs4 import BeautifulSoup


def get_bs_element(content: str) -> BeautifulSoup:
    bs = BeautifulSoup(content, "html.parser")
    return bs


def get_imgs_from_page(content: str) -> List[str]:
    result: List[str] = []
    bs = get_bs_element(content)
    return result


def universal_download(url, output_dir='.', **kwargs):
    pass


def download_htmls_from_index(url: str):
    pass


def download_single_html_content(url: str):
    """
    sort all imgs, download top size image
    """
    pass


prefer_download = download_single_html_content
prefer_download_list = download_htmls_from_index