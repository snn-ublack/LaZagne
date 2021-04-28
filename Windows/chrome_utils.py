#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : chrome_utils.py
# Author            : sinhnn <sinhnn>
# Date              : 28.04.2021
# Last Modified Date: 28.04.2021
# Last Modified By  : sinhnn <sinhnn>


import os
import traceback
from lazagne.softwares.browsers.chromium_based import ChromiumBased
from lazagne.softwares.browsers.mozilla import Mozilla

from lazagne.config.write_output import write_in_file, StandardOutput
from lazagne.config.manage_modules import get_categories
from lazagne.config.constant import constant
# from lazagne.config.run import run_lazagne, create_module_dic

from pathlib import Path
import sqlite3
import sqlite_utils

constant.st = StandardOutput()  # Object used to manage the output / write functions (cf write_output file)
constant.is_current_user = True

# from find_chrome_user_data_dir import find_chrome_user_data_dir
# import json
# import logging
# from functools import partial

# import mysql
# def mysql_bulkInsert(conn, data, table):
    # keys = data[0].keys()
    # stmt = "INSERT INTO {} ({}) VALUES ({}) as new ON DUPLICATE KEY UPDATE {}".format(
        # table,
        # ', '.join(keys),
        # ', '.join(["%s"]*len(keys)),
        # ", ".join(map(
            # lambda k: '{} = new.{}'.format(k, k),
            # filter(lambda k: k!= "id", keys)
        # ))
    # )
    # cursor = conn.cursor()
    # array = []
    # for r in data:
        # row = [];
        # for k in keys:
            # row.append(r[k])
        # array.append(row)
    # cursor.executemany(stmt, array)
    # conn.commit();
    # logging.debug(cursor.statement)

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


def extract_chrome_info(path):
    """TODO: Docstring for extract_chrome_info.

    :path: TODO
    :returns: TODO

    """
    b = ChromiumBased(browser_name=u'google chrome', paths=[path])
    accounts = b.run()
    cookies = b.cookies();
    c_user = None
    for cookie in cookies:
        if 'facebook.com' in cookie['host_key'] and cookie['name'] == "c_user":
            c_user = cookie["value"]
            break

    with open(os.path.join(path, "Default", "passwords.txt"), "a") as fp:
       fp.write("\n==================== {} ====================n".format(date.today()));
       fp.write('\n'.join([json.dumps(acc) for acc in accounts]));

    return {
            'path': Path(os.path.abspath(path)).as_posix(),
            'accounts': accounts,
            'cookies': cookies,
            'id': c_user,
            'c_user': c_user
            }


if __name__ == "__main__":
    import argparse
    from datetime import date
    import json

    parser = argparse.ArgumentParser(description="extract and backup chrome accounts and cookies")
    parser.add_argument("path", help="--user-data-dir")
    parser.add_argument("--scan", help="scan chrome directory in given path", action="store_true")
    parser.add_argument("--sqlite-file", help="target sqlite file")
    parser.add_argument("--table", help="target table to store data", type=str, default="chrome")
    parser.add_argument("--mysql-host", help="mysql host connection", type=str, default="localhost")
    parser.add_argument("--mysql-user", help="mysql host user", type=str, default="root")
    parser.add_argument("--mysql-password", help="mysql host user password", type=str, default="Zdr4g0nb4ll2")
    parser.add_argument("--mysql-table", help="target mysql table", type=str, default="chrome")
    args = parser.parse_args()

    paths = []
    if args.scan is True:
        find_chrome_user_data_dir(dest=paths, path=args.path)
    else:
        paths = [args.path]


    alls = [extract_chrome_info(c_path) for c_path in paths]
    if args.sqlite_file:
        db = sqlite_utils.Database(args.sqlite_file)
        db['chrome'].upsert_all(alls, pk="path", alter=True)
        db.close()

    with open('__all__.txt', 'a') as fp:
        fp.write(json.dumps(alls) + '\n')
