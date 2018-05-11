# -*- coding: utf-8 -*-
# @Author: JanKin Cai
# @Date:   2018-05-10 23:46:32
# @Last Modified by:   1249614072@qq.com
# @Last Modified time: 2018-05-10 23:46:51
import os
import sys
import pkgutil


def get_root_path(import_name):
    """
    Returns the path to a package or cwd if that cannot be found.  This
    returns the path of a package or the folder that contains a module.

    Not to be confused with the package path returned by :func:`find_package`.
    """
    mod = sys.modules.get(import_name)
    if mod is not None and hasattr(mod, '__file__'):
        return os.path.dirname(os.path.abspath(mod.__file__))

    loader = pkgutil.get_loader(import_name)

    if loader is None or import_name == '__main__':
        return os.getcwd()

    if hasattr(loader, 'get_filename'):
        filepath = loader.get_filename(import_name)
    else:
        __import__(import_name)
        mod = sys.modules.get(import_name)
        filepath = getattr(mod, '__file__', None)
        if filepath is None:
            raise RuntimeError('No root path can be found for the provided '
                               'module "%s".  This can happen because the '
                               'module came from an import hook that does '
                               'not provide file name information or because '
                               'it\'s a namespace package.  In this case '
                               'the root path needs to be explicitly '
                               'provided.' % import_name)
    return os.path.dirname(os.path.abspath(filepath))
