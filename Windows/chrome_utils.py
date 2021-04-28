#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  password_laZagne.py Author "sinhnn <sinhnn.92@gmail.com>" Date 21.05.2020


import os
import traceback
from lazagne.softwares.browsers.chromium_based import ChromiumBased
from lazagne.softwares.browsers.mozilla import Mozilla

from lazagne.config.write_output import write_in_file, StandardOutput
from lazagne.config.manage_modules import get_categories
from lazagne.config.constant import constant
# from lazagne.config.run import run_lazagne, create_module_dic

constant.st = StandardOutput()  # Object used to manage the output / write functions (cf write_output file)
constant.is_current_user = True

from pathlib import Path
import sqlite3
from find_chrome_user_data_dir import find_chrome_user_data_dir
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


if __name__ == "__main__":
    import argparse
    from datetime import date
    import json

    parser = argparse.ArgumentParser(description="extract and backup chrome accounts and cookies")
    parser.add_argument("path", help="--user-data-dir")
    parser.add_argument("--scan", help="Help text", action="store_true")
    parser.add_argument("--sqlite-file", help="Help text")
    parser.add_argument("--table", help="Help text", type=str, default="chrome")
    parser.add_argument("--mysql-host", help="Help text", type=str, default="localhost")
    parser.add_argument("--mysql-user", help="Help text", type=str, default="root")
    parser.add_argument("--mysql-password", help="Help text", type=str, default="Zdr4g0nb4ll2")
    parser.add_argument("--mysql-table", help="Help text", type=str, default="chrome")
    args = parser.parse_args()
    
    paths = []
    if args.scan is True:
        find_chrome_user_data_dir(dest=paths, path=args.path)
    else:
        paths = [path]

    alls = []
    for c_path in paths:
        b = ChromiumBased(browser_name=u'google chrome', paths=[c_path])
        accounts = b.run()
        cookies = b.cookies();
        c_user = None
        for cookie in cookies:
            if 'facebook.com' in cookie['host_key'] and cookie['name'] == "c_user":
                c_user = cookie["value"]
                break
    
        with open(os.path.join(c_path, "Default", "passwords.txt"), "a") as fp:
           fp.write("\n=================={}==========================\n".format(date.today()));
           fp.write('\n'.join([json.dumps(acc) for acc in accounts]));
        unix_path = Path(os.path.abspath(c_path)).as_posix()
        alls.append({'path': unix_path, 'accounts': accounts, 'cookies': cookies })

        if args.sqlite_file:
            conn = sqlite3.connect(args.sqlite_file)
            conn.execute("CREATE TABLE IF NOT EXISTS chrome (path TEXT PRIMARY KEY, accounts TEXT, cookies TEXT, c_user TEXT, id TEXT)")
            conn.execute("INSERT OR REPLACE INTO chrome (path, accounts, cookies, c_user, id) VALUES(?, ?, ?, ?, ?)",
                (unix_path, json.dumps(accounts), json.dumps(cookies), c_user, c_user)
            )
            conn.commit()
            conn.close()

    with open('__all__.txt', 'a') as fp:                
        fp.write(json.dumps(alls) + '\n')
