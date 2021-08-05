#!/usr/bin/env python3
import sys
import pandas as pd
from pandasql import sqldf


def main():
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    # const = sum, default = max,
    # help = 'sum the integers (default: find the max)')
    # print([*parser.parse_args()])

    day = "'2018-12-08'"
    cookie_log = pd.read_csv('cookie_log.csv')
    most_active_df = sqldf(f"""
    with counts as
    (select cookie, count(1) as count
    from cookie_log
    where date(timestamp) = {day}
    group by cookie
    )
    select cookie from counts
    where count = (select max(count) from counts)
    """, locals())
    print(most_active_df)


if __name__ == "__main__":
    main()
