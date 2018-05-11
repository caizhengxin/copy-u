# -*- coding: utf-8 -*-
# @Author: JanKin Cai
# @Date:   2018-05-10 23:27:05
# @Last Modified by:   caizhengxin16@163.com
# @Last Modified time: 2018-05-11 10:56:01
import config
from autocopy.auto import AutoCopy


autocopy = AutoCopy(__name__)
autocopy.config.from_object(config)


if __name__ == '__main__':
    autocopy.run()
