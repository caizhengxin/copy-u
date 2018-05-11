# -*- coding: utf-8 -*-
# @Author: JanKin Cai
# @Date:   2018-05-10 22:56:39
# @Last Modified by:   caizhengxin16@163.com
# @Last Modified time: 2018-05-11 10:13:10
from autocopy._compat import basestring


class Config(dict):

    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_object(self, obj):
        """
        """
        if isinstance(obj, basestring):
            raise TypeError()

        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
