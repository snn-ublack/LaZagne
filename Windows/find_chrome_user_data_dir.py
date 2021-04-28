#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  find_chrome_user_data_dir.py Author "sinhnn <sinhnn>" Date 22.04.2021

import os
import json


def find_chrome_user_data_dir(dest=[], path='.', maxdepth=-1):
    '''
    Return directory as a dictionary
        afilter : custom filter with DirEntry as only input
    Example: tree(dest=dest,path='.', maxdepth=-1, afilter=lambda x : x.name == 'wanted')
    '''
    def is_chrome_user_data_dir(d):
        for p in os.listdir(d):
            if p == u"Local State":
                return True
        return False

    if maxdepth == 0 or not len(list(os.scandir(path))):
        return

    for p in os.scandir(path):
        if p.is_file():
            continue
        if p.is_dir():
            if is_chrome_user_data_dir(p):
                dest.append(p.path)
                continue
            #  dest.append(find_chrome_user_data_dir(dest=[], path=p.path, maxdepth=maxdepth-1))
            find_chrome_user_data_dir(dest=dest, path=p.path, maxdepth=maxdepth-1)
    return

if __name__ == "__main__":
    dest= []
    find_chrome_user_data_dir(dest, '/home/sinhnn/.config')
    print(dest)
