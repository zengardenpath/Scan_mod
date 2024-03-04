#!/usr/bin/env python

import os
import sys
import timeit
import datetime
import glob
import pyclbr
import inspect
import argparse
from operator import itemgetter
from os.path import basename, dirname, abspath


class ScanModule:
    @classmethod
    def show_classes(cls, name, class_data):
        print("Class:", name)
        filename = basename(class_data.file)
        print(f"\tFile: {filename} [{class_data.lineno}]")

        cls.show_super_classes(class_data)
        cls.show_methods(class_data)
        print()
        return

    @staticmethod
    def show_methods(class_data):
        for name, lineno in sorted(class_data.methods.items(),
                                   key=itemgetter(1)):
            print(f"\tMethod: {name} [{lineno}]")
        return

    @staticmethod
    def show_super_classes(class_data):
        super_class_names = []
        for super_class in class_data.super:
            if super_class == "object":
                continue
            if isinstance(super_class, str):
                super_class_names.append(super_class)
            else:
                super_class_names.append(super_class.name)

        if super_class_names:
            print(f"\tSuper classes:{super_class_names}")
        return


def main():
    parser = argparse.ArgumentParser(description="scan python \
                source to find classes and stand-alone functions ",
                                     epilog="scan_module.py -f <python file> | <path>/*.py")

    parser.add_argument("-f", "--file", action="store",
                        nargs="*", dest="input_file", default=[],
                        help="specify one or more scan files.If \
                         no value is specified for this argument,\
                         it will scan all modules in the current \
                         directory. This is an optional argument.")

    results = parser.parse_args()

    if len(results.input_file) == 0:
        for name in glob.glob("%s/*.py" % os.path.curdir):
            results.input_file.append(name)

    for f in results.input_file:
        fp = dirname(abspath(f))
        sys.path.append(fp + os.path.sep)

    _sep = "."
    _modules_list = list(map(lambda x: basename(x).split(_sep)[0],
                             results.input_file))
    _modules_len = len(_modules_list)

    for fi in _modules_list:
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print(f"\033[2;31m{time_now} Start scanning module: {fi}\033[0m")

        example_data = pyclbr.readmodule(fi)
        print(f"example_data --> {example_data}")
        if example_data:
            for name, class_data in sorted(example_data.items(),
                                           key=lambda x: x[1].lineno):
                print(f"name: {name}, class_data: {class_data}")
                ScanModule.show_classes(name, class_data)
        else:
            module = __import__(fi)
            all_functions = inspect.getmembers(module, inspect.isfunction)
            print(f"File: {module}")
            for func in all_functions:
                print(f"\tMethod: {func[0]}")
            print()
    print(f"Scanned {_modules_len} modules.")


if __name__ == "__main__":
    print(f"Execution time: {timeit.timeit('main()', 'from __main__ import main', number=1)}")
