#!/usr/bin/env python

from __future__ import division, print_function

import sys
import yaml
import bisect
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict


INDENT = 4 * " "


def line_split(line):
    lst = line.split(None, 2)
    time_range = lst[0]
    category = lst[1]
    try:
        desc = lst[2]
    except IndexError:
        desc = ""
    return time_range, category, desc


def parse_time_range(time_range_str):
    start, end = time_range_str.split("--")
    return start, end


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d (%A)")


def parse_hours(hours_lst):
    values = []
    for line in hours_lst:
        time_range, category, description = line_split(line)
        start, end = parse_time_range(time_range)
        values.append((start, end, category, description))
    return values


def find_leftmost_index(lst, start_date):
    """Find leftmost index greater than or equal to start_date"""
    i = bisect.bisect_left(lst, start_date)
    if i != len(lst):
        return i
    raise ValueError


def find_rightmost_index(lst, end_date):
    """Find rightmost value less than end_date"""
    i = bisect.bisect_left(lst, end_date)
    if i:
        return i
    raise ValueError


def window_data(data, start_date, end_date):
    keylist = list(data.keys())
    start_index = find_leftmost_index(keylist, start_date)
    stop_index = find_rightmost_index(keylist, end_date)
    windowed = OrderedDict()
    for key in keylist[start_index:stop_index]:
        windowed[key] = data[key]
    return windowed


def parse(filename="daily.yaml"):
    with open(filename) as fh:
        hours_doc = yaml.load(fh)

    data = {}
    for date_str, hours_lst in hours_doc.items():
        date = parse_date(date_str)
        hours = parse_hours(hours_lst)
        data[date] = hours

    return OrderedDict(sorted(data.items()))


def normalize_dates(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    return start_date, end_date


def time_diff(end, start):
    """Take two times formatted HHMM and return end-start, in hours."""
    end = 60 * int(end[:2]) + int(end[2:])
    start = 60 * int(start[:2]) + int(start[2:])
    return float(end-start) / 60


def bin_hours(hours):
    time_from_category = defaultdict(int)
    desc_from_category = defaultdict(list)
    for logline in hours:
        start, end, category, description = logline
        time = time_diff(end, start)
        category = category.strip().lower()
        if category == 'break':
            continue
        time_from_category[category] += time
        desc_from_category[category].append(description)

    combined = {}
    for key in time_from_category:
        combined[key] = time_from_category[key], desc_from_category[key]
    return combined


def build_hours_from_date(data):
    hours_from_date = OrderedDict()
    for date, hours in data.items():
        hours_from_date[date] = bin_hours(hours)
    return hours_from_date


def print_hours(hours_from_date):
    for date in hours_from_date:
        print(datetime.strftime(date, "%Y-%m-%d (%A):"))
        current = hours_from_date[date]
        for category in sorted(current.keys()):
            hours = current[category][0]
            line = "{}{:5.2f} {}".format(INDENT, hours, category)
            print(line)


def build_desc_from_category(hours_from_date):
    desc_from_category = defaultdict(list)
    for date in hours_from_date:
        for category in hours_from_date[date]:
            for desc_line in hours_from_date[date][category][1]:
                desc_from_category[category].append(desc_line)
    return desc_from_category


def print_categories(desc_from_category):
    print("Projects billed:")
    for category in sorted(desc_from_category.keys()):
        print("{}{}".format(INDENT, category))


def print_desc_from_category(desc_from_category):
    for category in sorted(desc_from_category.keys()):
        print()
        print(category)
        for line in desc_from_category[category]:
            if line.strip():
                print("- {}".format(line))


def build_hours_from_category(hours_from_date):
    hours_from_category = defaultdict(int)
    for date in hours_from_date:
        for category in hours_from_date[date]:
            hours_from_category[category] += hours_from_date[date][category][0]
    return hours_from_category


def print_hours_from_category(hours_from_category):
    for category in sorted(hours_from_category.keys()):
        print(category, hours_from_category[category])


def all_categories(hours_from_date):
    categories = set()
    for date in hours_from_date:
        for category in hours_from_date[date]:
            categories.add(category)
    return sorted(categories)


def print_hours_table(hours_from_date, hours_from_category):
    dates = hours_from_date.keys()
    categories = all_categories(hours_from_date)
    cat_width = 22

    # print column titles
    print(" "*cat_width, end="  ")
    for date in dates:
        print(date.strftime("%m-%d"), end=" ")
    print("Total", end="")

    # print underlines
    print()
    print(" "*cat_width, end="  ")
    for date in dates:
        print(date.strftime("-----"), end=" ")
    print(date.strftime("-----"), end="")

    # print line per billing category
    print()
    for category in categories:
        print(("{:" + str(cat_width) + "s}").format(category), end=": ")
        for date in dates:
            fmt = "{:5.2f}"
            if category not in hours_from_date[date]:
                print(fmt.format(0.0), end=" ")
            else:
                print(fmt.format(hours_from_date[date][category][0]), end=" ")
        print(fmt.format(hours_from_category[category]), end="")
        print()

    # print line for totals
    print(("{:" + str(cat_width) + "s}").format("Total"), end=": ")
    total_of_totals = 0
    fmt = "{:5.2f}"
    for date in dates:
        cats = hours_from_date[date]
        total = sum([val[0] for val in cats.values()])
        total_of_totals += total
        print(fmt.format(total), end=" ")
    print(fmt.format(total_of_totals), end="")


def setup(path, start_date, end_date):
    data = parse(path)
    start, end = normalize_dates(start_date, end_date)
    windowed = window_data(data, start, end)

    hours_from_date = build_hours_from_date(windowed)
    desc_from_category = build_desc_from_category(hours_from_date)
    return windowed, hours_from_date, desc_from_category


def main(path, start_date, end_date):
    _, hours_from_date, desc_from_category = setup(path, start_date, end_date)
    hours_from_category = build_hours_from_category(hours_from_date)
    print()
    print_hours_table(hours_from_date, hours_from_category)
    print()
    print_desc_from_category(desc_from_category)


def last_week(path):
    today = datetime.today()
    last_sunday = today - timedelta(days=(today.weekday()+1))
    previous_sunday = last_sunday - timedelta(days=7)
    end_date = last_sunday.strftime("%Y-%m-%d")
    start_date = previous_sunday.strftime("%Y-%m-%d")
    return start_date, end_date


def this_week(path):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    last_sunday = today - timedelta(days=(today.weekday()+1))
    end_date = tomorrow.strftime("%Y-%m-%d")
    start_date = last_sunday.strftime("%Y-%m-%d")
    return start_date, end_date


def yesterday(path):
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    end_date = today.strftime("%Y-%m-%d")
    start_date = yesterday.strftime("%Y-%m-%d")
    return start_date, end_date


def today(path):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    end_date = tomorrow.strftime("%Y-%m-%d")
    start_date = today.strftime("%Y-%m-%d")
    return start_date, end_date


def cli():
    if len(sys.argv) == 4:
        path, start_date, end_date = sys.argv[1:]
    elif len(sys.argv) == 2:
        # assume the nearest previous Sunday through today
        path = sys.argv[1]
        start_date, end_date = this_week(path)
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        time = sys.argv[2]
        keys = {'last_week': last_week,
                'week': this_week,
                'yesterday': yesterday,
                'today': today,
                }
        start_date, end_date = keys[time](path)

    main(path, start_date, end_date)


if __name__ == "__main__":
    cli()
