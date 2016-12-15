# !/usr/bin/env python
# coding: utf-8
import requests
import time
import random
from copy import deepcopy
from pyquery import PyQuery
import re
from lib.http import *
from lib.files import *
from setting import *

default_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

post_headers = deepcopy(default_headers)
post_headers.update({
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://www.verycd.com/'
})

detail_page_url = 'http://www.verycd.com/topics/{}/'
comment_url = 'http://www.verycd.com/ajax/folder/comments?id={}'



def get_comment(urls):
    '''
    获取verycd的评论
    :param urls:            list            一个topic的url list
    :return:                list
    '''
    session = requests.session()
    content_list = []
    for url in urls:
        res = http_requst_with_sleep(session, url, headers=default_headers)
        comment = re.findall('<!--Wrap-head end-->(.*?)<!--Wrap-tail begin-->', res.text)
        content_list.extend([i.strip() for i in comment if len(i) < 128])
    return content_list


def get_link(url, page=10):
    session = requests.session()
    url_list = []

    for i in range(1, page):
        res = http_requst_with_sleep(session, url.format(i), headers=default_headers)
        pq = PyQuery(res.content)
        for a in pq('h3 a').items():
            url_list.append(a.attr('href'))
    return [re.search('(\d+)', i).group(1) for i in url_list]


def dump_link(page=post_comment_page):
    url = post_comment_where
    dump_pkl(comment_url_path, get_link(url, page))


def dump_comment(page=get_comment_where):
    url = get_comment_where
    dump_files(comment_text_path, get_link(url, page))


def load_content():
    return load_files(comment_text_path)


def load_url():
    return load_pkl(comment_url_path)


def login_and_reply(user_list):
    for each_user in user_list:
        user, pw = each_user
        session = requests.session()
        res = http_request(session, 'http://www.verycd.com/', headers=post_headers)
        data = {
            'username': user,
            'password': pw,
            'save_cookie': '1',
            'login_submit': '登录',
            'continue': 'http://www.verycd.com',
        }

        res = http_request(
            session,
            'http://secure.verycd.com/signin',
            method='POST',
            headers=post_headers,
            data=data,
            allow_redirects=False
        )

        content = load_content()
        url_list = load_url()

        for count in range(comment_each_time):
            tid = random.choice(url_list)
            comment = random.choice(content)
            print comment
            print tid

            files = {
                'contents': (None, comment),
                'use_bbcode': (None, '1'),
                'tid': (None, tid),
            }
            new_headers = deepcopy(post_headers)
            new_headers.update({
                'Referer': 'http://www.verycd.com/topics/{}/'.format(tid)
            })
            res = http_request(
                session,
                'http://www.verycd.com/topics/{}/reply'.format(tid),
                method='POST',
                headers=new_headers,
                files=files,
                allow_redirects=False
            )
            print res.status_code
            time.sleep(sleep_time)
