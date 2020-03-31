#! -*- coding: utf-8 -*-

import os, random
import time
import re
from urllib import request, parse
import socket
from typing import List, Dict, Optional, Any, Union, Tuple
import requests
# from cartoon.util import log

UA_LIST: List[str] = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

FAKE_HEADER: Dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa
    "Accept-Charset": "UTF-8,*;q=0.5",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",  # noqa
}

def get_header() -> Dict[str, str]:
    new_ = FAKE_HEADER.copy()
    new_["User-Agent"] = random.choice(UA_LIST)
    return new_

# global variables
def match1(text: str, *patterns: Any) -> Union[List[str], None]:

    ret: List[str] = []
    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            ret.append(match.group(1))
        else:
            return None
    else:
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
    return ret


def get_with_retry(*args, **kwargs):
    """
    fetch url with retry times
    args & kwargs for request.urlopen
    """
    retry_time = 3
    relay_step = 5
    for i in range(retry_time):
        try:
            response = requests.get(*args, **kwargs)
            return response
        except Exception as e:
            time.sleep(i * relay_step)
            if i + 1 == retry_time:
                raise e


def get_content(url: str, headers: Optional[Dict[str, str]] = None) -> bytes:
    """
    get url content

    Return: bytes
    """
    content = requests.get(url, headers=headers or get_header()).content
    return content


def post_content(
    url: str, headers: Optional[Dict[str, str]] = None, post_data: Dict[str, Any] = {}, **kwargs
) -> bytes:
    content = requests.post(url, headers=headers or get_header(), json=post_data).content
    return content


def urls_save(
    url_names: List[Tuple[str, str]],
    dir_name: str,
    headers: Optional[Dict[str, str]] = None,
    refer: Optional[str] = None,
    timeout: Optional[float] = None,
    **kwargs
):
    """
    save urls to dir_name

    Args:
        url_names:  Tuple contains [img_url, file_name]
        dir_name: the directory will created
        headers: request header
        refer: refer if needed
        timeout: timeout 
    """
    cur_path = os.getcwd()
    if os.path.exists(dir_name):
        return
    temp_dirname = "." + dir_name
    if not os.path.exists(temp_dirname):
        os.mkdir(temp_dirname)
    os.chdir(temp_dirname)
    # log.i("chdir to " + temp_dirname)
    for u, n in url_names:
        url_save(u, n, headers=headers, refer=u, timeout=timeout, **kwargs)
    # rename
    os.chdir(cur_path)
    os.rename(temp_dirname, dir_name)


def url_save(
    url: str,
    filepath: str,
    headers: Optional[Dict[str, str]] = None,
    refer: Optional[str] = None,
    timeout: Optional[float] = None,
    **kwargs
):
    temp_headers: Dict[str, str] = headers or get_header()
    if refer is not None:
        temp_headers.setdefault("refer", refer)

    if isinstance(url, list):
        # file_size = urls_size(url, temp_headers)
        is_chunked, urls = True, url
    else:
        # file_size = url_size(url, temp_headers)
        is_chunked, urls = False, [url]

    open_mode = "wb"
    temp_filename = filepath + ".download"  # if file_size != float("inf") else filepath
    # received: int = 0

    for url in urls:
        if os.path.exists(filepath):
            continue
        try:
            response = requests.get(url, headers=headers or get_header(), timeout=timeout)
        except Exception as e:
            print(e)
            continue
        # log.i("saving " + url + " -> " + temp_filename)
        with open(temp_filename, open_mode) as output:
            output.write(response.content)

        if os.access(filepath, os.W_OK):
            os.remove(filepath)
        os.rename(temp_filename, filepath)
