# !/usr/bin/env python
# coding: utf-8
import time
import md5
import os
import random
from setting import sleep_each_request

def http_requst_with_sleep(session, url, retry=10, method='GET', retry_sleep_time=5, **kwargs):
    time.sleep(sleep_each_request)
    return http_request(session, url, retry=retry, method=method, retry_sleep_time=retry_sleep_time, **kwargs)

def http_request(session, url, retry=10, method='GET', retry_sleep_time=5, **kwargs):
    no_more_try = False
    now_retry = 0
    res = None

    while not no_more_try:
        try:
            if method == 'GET':
                res = session.get(url, **kwargs)
            elif method == 'POST':
                res = session.post(url, **kwargs)
            if 200 <= res.status_code <= 399:
                break
        except Exception as e:
            print str(e)
            if now_retry < retry:
                now_retry += 1
            else:
                no_more_try = True
            time.sleep(retry_sleep_time)
    return res


def open_browser(html, browser='firefox'):
    name = md5.new(str(time.time()) + str(random.randint(0, 9999999))).hexdigest()
    path = '/tmp/' + name + '.html'
    with open(path, 'wb') as f:
        f.write(html)
    os.system(browser + ' ' + path)