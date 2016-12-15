# !/usr/bin/env python
# coding: utf-8
import cPickle


def load_files(path):
    with open(path, 'r') as f:
        content = f.read()
    return content.split('\n')


def dump_files(path, list_):
    with open(path, 'w') as f:
        for i in list_:
            f.write(i + '\n')


def load_pkl(path):
    return cPickle.load(open(path, "rb"))


def dump_pkl(path, obj):
    cPickle.dump(obj, open(path, 'wb'))
