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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

post_headers = deepcopy(default_headers)
post_headers.update({
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://www.verycd.com/',
    'X-Requested-With': 'XMLHttpRequest'
})

detail_page_url = 'http://www.verycd.com/topics/{}/'
comment_url = 'http://www.verycd.com/ajax/folder/comments?id={}'


def get_comment(tid, session=None):
    session = requests.session() if not session else session

    print 'getting {} comment'.format(tid)
    res = http_requst_with_sleep(session, comment_url.format(tid), headers=default_headers)
    comment = re.findall('<!--Wrap-head end-->(.*?)<!--Wrap-tail begin-->', res.text)

    return [i.strip() for i in comment if len(i) < 128]


def get_link(url, session=None):
    session = requests.session() if not session else session

    print 'getting {} links'.format(url.format(url))
    res = http_requst_with_sleep(session, url.format(url), headers=default_headers)
    pq = PyQuery(res.content)

    tids = []
    for a in pq('h3 a').items():
        tids.append(re.search('(\d+)', a.attr('href')).group(1))
    return tids


def dump_link(page=post_comment_page):
    url = post_comment_where
    for p in range(1, page + 1):
        dump_files(comment_url_path, get_link(url.format(p)))


def dump_comment(page=get_comment_page):
    url = get_comment_where
    for p in range(1, page + 1):
        tids = get_link(url.format(p))
        for tid in tids:
            dump_files(comment_text_path, get_comment(tid))


def load_content():
    return load_files(comment_text_path)


def load_url():
    return load_pkl(comment_url_path)


def login_and_reply(user_list):
    for each_user in user_list:
        user, pw = each_user
        print 'user:' + user
        print 'login..'
        session = requests.session()
        res = http_request(session, 'http://www.verycd.com/', headers=post_headers)

        print '{} get session'.format(res.status_code)

        data = {
            'username': user,
            'password': pw,
            'save_cookie': '1',
        }

        res = http_request(
            session,
            'http://secure.verycd.com/signin',
            method='POST',
            headers=post_headers,
            data=data,
            allow_redirects=False
        )
        print '{} login success.'.format(res.status_code)

        content = load_content()
        url_list = load_url()

        for count in range(comment_each_time):
            tid = random.choice(url_list)
            comment = random.choice(content)
            print 'comment:{}'.format(comment)
            print 'topic_id:{}'.format(tid)

            files = {
                'contents': (None, comment),
                'use_bbcode': (None, '1'),
                'tid': (None, tid),
            }
            new_headers = deepcopy(default_headers)
            new_headers.update({
                'Referer': 'http://www.verycd.com/topics/{}/'.format(tid),
            })
            res = http_request(
                session,
                'http://www.verycd.com/topics/{}/reply'.format(tid),
                method='POST',
                headers=new_headers,
                files=files,
                allow_redirects=False
            )

            print '{} post comment.'.format(res.status_code)
            time.sleep(sleep_time)
