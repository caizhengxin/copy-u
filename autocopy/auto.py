# -*- coding: utf-8 -*-
# @Author: JanKin Cai
# @Date:   2018-05-10 22:34:07
# @Last Modified by:   caizhengxin16@163.com
# @Last Modified time: 2018-05-11 14:46:43
import os
import shutil

import win32file
from werkzeug.datastructures import ImmutableDict
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from autocopy.config import Config
from autocopy._compat import basestring, integer_types


class AutoCopy(object):

    config_class = Config

    default_config = ImmutableDict({
        'DEBUG': False,
        'DRIVE_LIST': [],
        'DST_PATH': 'C:\\autocopy',
        'EXTENSION': ['.txt'],
        'FILE_SIZE': "10 MB",
        'SECONDS': 2,
        'UNIT': {
            "KB": 1024,
            "MB": 1024 * 1024,
            "GB": 1024 * 1024 * 1024
        }
    })

    def __init__(self, import_name, *args, **kwargs):
        self.import_name = import_name
        self.get_logica_drives = win32file.GetLogicalDrives
        self.config = self.make_config()
        self.scheduler = BlockingScheduler()

    def init(self):
        self.drive_list = self.config.get('DRIVE_LIST')
        self.dst_path = self.config.get('DST_PATH')
        self.unit = self.config.get('UNIT')
        self.size = self.config.get('FILE_SIZE')
        self.extension = self.config.get('EXTENSION')
        self.seconds = self.config.get('SECONDS')
        self.is_dst_path()

    def make_config(self):
        return self.config_class(self.default_config)

    def is_u_disk(self, drive, drive_num=2):
        return win32file.GetDriveType(drive) == drive_num

    def get_u_disk(self, drive_list=None):
        sign = self.get_logica_drives()
        drive_list = drive_list or self.drive_list

        drives = (drive_list[i] for i in range(len(drive_list) - 1) if (
            sign & 1 << i and self.is_u_disk(drive_list[i])))

        return drives

    def is_dst_path(self, dst_path=None):
        dst_path = dst_path or self.dst_path

        if not os.path.exists(dst_path) or not os.path.isdir(dst_path):

            try:
                os.mkdir(dst_path)
            except Exception:
                os.remove(dst_path)
                os.mkdir(dst_path)

        return None

    def _get_size(self, size, unit='KB'):
        units = self.unit

        if isinstance(size, integer_types):
            return size * units.get(unit, 1024)

        try:
            size, unit = size.split(' ')
        except Exception:
            pass
        else:
            return int(size) * units.get(unit, 1024)

        return 1024

    def is_file_size(self, file, size=None):
        if not isinstance(file, basestring):
            raise TypeError("This is not a string.")

        size = size or self.size

        return os.path.getsize(file) < self._get_size(size=size)

    def _copyfile(self, path, dst_path=None, extension=None):

        for path, _, file_list in os.walk(path):
            for file in file_list:
                _, ext = os.path.splitext(file)
                file = os.path.join(path, file)
                if ext in extension and self.is_file_size(file):
                    try:
                        shutil.copy(file, dst_path)
                    except Exception:
                        self.is_dst_path()

    def copyfile(self, dst_path=None, extension=None):
        extension = extension or self.extension
        dst_path = dst_path or self.dst_path
        drives = self.get_u_disk()

        for drive in drives:
            self._copyfile(drive, dst_path, extension)

    def _run(self, *args, **kwargs):
        self.copyfile(*args, **kwargs)

    def run(self, timer=True, seconds=None, *args, **kwargs):
        self.init()

        if not timer:
            return self._run

        trigger = IntervalTrigger(seconds=seconds or self.seconds)
        self.scheduler.add_job(self._run, trigger)
        # self.scheduler.add_job()

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()


if __name__ == '__main__':
    pass
