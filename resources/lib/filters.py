# -*- coding: utf-8 -*-
# Module: default
# Author: jurialmunkey
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import operator
from jurialmunkey.parser import split_items


FILTER_KEYNAMES = ('filter_key', 'filter_value', 'filter_operator', 'exclude_key', 'exclude_value', 'exclude_operator', )


def get_filters(**kwargs):
    all_filters = {}

    for k, v in kwargs.items():
        key, num = k, '0'
        if '__' in k:
            key, num = k.split('__', 1)
        if key not in FILTER_KEYNAMES:
            continue
        dic = all_filters.setdefault(num, {})
        dic[key] = v

    return all_filters


def is_excluded(item, filter_key=None, filter_value=None, filter_operator=None, exclude_key=None, exclude_value=None, exclude_operator=None):
    """ Checks if item should be excluded based on filter/exclude values
    Values can optional be a dict which contains module, method, and kwargs
    """
    def is_filtered(d, k, v, exclude=False, operator_type=None):
        comp = getattr(operator, operator_type or 'contains')
        boolean = False if exclude else True  # Flip values if we want to exclude instead of include
        if k and v and k in d and comp(str(d[k]).lower(), str(v).lower()):
            boolean = exclude
        return boolean

    if not item:
        return

    il, ip = item.get('infolabels', {}), item.get('infoproperties', {})

    if filter_key and filter_value:
        _exclude = True
        for fv in split_items(filter_value):
            _exclude = True
            if filter_key in il:
                _exclude = False
                if is_filtered(il, filter_key, fv, operator_type=filter_operator):
                    _exclude = True
                    continue
            if filter_key in ip:
                _exclude = False
                if is_filtered(ip, filter_key, fv, operator_type=filter_operator):
                    _exclude = True
                    continue
            if not _exclude:
                break
        if _exclude:
            return True

    if exclude_key and exclude_value:
        for ev in split_items(exclude_value):
            if exclude_key in il:
                if is_filtered(il, exclude_key, ev, True, operator_type=exclude_operator):
                    return True
            if exclude_key in ip:
                if is_filtered(ip, exclude_key, ev, True, operator_type=exclude_operator):
                    return True
