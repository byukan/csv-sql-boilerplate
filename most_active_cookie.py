#!/usr/bin/env python3
"""
:file: most_active_cookie.py
:author: Brant Yukan
:date: 8/4/21
:brief: This program processes the cookie log and returns the most active cookie for specified day.
$ ./most_active_cookie cookie_log.csv -d 2018-12-08
"""
import csv
import os
import sqlite3
import sys


def csv_to_db(csv_file):
    """
    This function stores the table to a database on disk.
    :param csv_file: data table with column headings
    :return:
    """
    with open('cookie_log.csv') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)
        to_db = [(x['cookie'], x['timestamp']) for x in dr]
    db_file = csv_file.rsplit('.', 1)[0] + '.db'
    open(db_file, 'w')
    con = sqlite3.connect(db_file)  # store db on disk, alternatively :memory: stores in RAM
    cur = con.cursor()
    cur.execute('CREATE TABLE cookie_log (cookie, timestamp);')
    cur.executemany("INSERT INTO cookie_log (cookie, timestamp) VALUES (?, ?);", to_db)
    con.commit()
    con.close()


def query_db(db_file, query):
    """
    This function runs the query on the .db file by spinning up a sqlite connection.
    :param query:
    :param db_file: .db file
    :return: Connection to db, Cursor to executed query
    """
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    return con, cur.execute(query)


def main():
    csv_file, day = sys.argv[1], sys.argv[3]
    db_file = csv_file.rsplit('.', 1)[0] + '.db'
    # if os.path.exists(db_file):
    #     os.remove(db_file)

    if not os.path.exists(db_file):
        csv_to_db(csv_file)

    query = f"""
            WITH counts AS (SELECT cookie,
                            Count(1) AS count
                     FROM   cookie_log
                     WHERE  Date(timestamp) = '{day}'
                     GROUP  BY cookie)
            SELECT cookie FROM counts
            WHERE  count = (SELECT Max(count) FROM counts)
            """

    con, cur_execute = query_db(db_file, query)

    top_cookies = {x[0] for x in cur_execute}
    for x in top_cookies:
        print(x)

    con.close()

    return top_cookies


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        main()
    else:
        print('Usage: ./most_active_cookie.py log.csv -d yyyy-mm-dd')
