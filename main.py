# !/usr/bin/env python
# coding: utf-8
import logging
from core.spider import login_and_reply, dump_comment, dump_link
from setting import user_list


if __name__ == '__main__':
    login_and_reply(user_list)
    # dump_comment(2)
