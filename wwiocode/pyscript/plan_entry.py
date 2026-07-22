#!/usr/bin/python3

import os
import sys

import plan_util as UTIL


sys.path.append("/opt/userdata/crm/src/python/opsutil")

import ArgMap
import CodeSetup as SETUP


class ProcessDocTool:

    def run_op(self, argmap):


        docinfo = UTIL.load_doc_info()

        #print(docinfo)

        UTIL.insert_doc_info()


class BasicTool:

    def run_op(self, argmap):
        print("Study basic!!!")

        print(f"Work directory is {UTIL.WORK_DIR}")

        assert os.path.exists(UTIL.WORK_DIR)


if __name__ == '__main__':

    SETUP.configure(globals())

    mytool, argmap = SETUP.driver_and_argmap()
    mytool.run_op(argmap)