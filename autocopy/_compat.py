# -*- coding: utf-8 -*-
# @Author: caixin
# @Date:   2018-01-28 15:17:37
# @Last Modified by:   caizhengxin16@163.com
# @Last Modified time: 2018-05-11 09:09:45
"""
Python 2.6, 2.7, and 3.x compatibility.

"""
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

PY35 = sys.version_info[:2] == (3, 5)
PY36 = sys.version_info[:2] == (3, 6)


if PY3:
    basestring = str,
    integer_types = int,
    unicode = str
    unichr = chr
    _range = range
else:
    integer_types = (int, long)
    _range = xrange


if __name__ == '__main__':
    pass
