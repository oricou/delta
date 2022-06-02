import math
import numpy as np
from dash import html
from typing import OrderedDict
from functools import reduce
from ps_ap_chessgames.src.labels import max_grps_nb


def compute_range(df, x_axis, step):
    lower = step * math.floor(df[x_axis].min() / step)
    upper = step * math.ceil(df[x_axis].max() / step)
    return np.arange(lower, upper, step)


def to_int_list(to_convert):
    try:
        return list(map(int, to_convert))
    except ValueError:
        return [math.inf]


def drop_smallest_grp(grps, column, grp_selector=None):
    if grps.ngroups <= max_grps_nb:
        return grps
    grp_selector = column if grp_selector is None else grp_selector
    last_most_used = grps.size().sort_values(ascending=False).iloc[max_grps_nb]
    last_most_used = 1 if last_most_used <= 0 else last_most_used
    return grps.filter(lambda grp: grp[column].count() >= last_most_used).groupby(
        grp_selector, sort=False
    )


def get_largest_grp(grps):
    ordered_grps = grps.size().sort_values(ascending=False)
    return ordered_grps.idxmax(), ordered_grps.max()


def to_html_list(datas):
    items = []
    for desc, data in datas.values():
        if issubclass(type(data), OrderedDict):
            items.append(html.Li(desc))
            items.append(to_html_list(data))
        else:
            items.append(html.Li(desc + str(data)))
    return html.Ul(items)


def count(grp, column, str):
    if str is not None:
        return grp[column].apply(
            lambda x: x[x == str].count() if x[x == str] is not None else 0
        )
    return grp[column].count()


def compute_rate(grp, dividend_str, divisor_str, column):
    if dividend_str is None or type(dividend_str) is str:
        dividend = count(grp, column, dividend_str)
    else:
        counts = [count(grp, column, str) for str in dividend_str]
        dividend = reduce(lambda x, y: x.add(y, fill_value=0), counts)

    if divisor_str is None or type(divisor_str) is str:
        divisor = count(grp, column, divisor_str)
    else:
        counts = [count(grp, column, str) for str in divisor_str]
        divisor = reduce(lambda x, y: x.add(y, fill_value=0), counts)

    return (dividend / (divisor + dividend)) * 100
