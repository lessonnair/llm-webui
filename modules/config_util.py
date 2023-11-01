# -*- coding: utf-8 -*-

import configparser
import json
import pandas as pd
import re
from util import *

def read_config_file(config_path):
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(config_path)
    return config

class TaskConfig(object):

    def __init__(self, config_path):
        self.config = read_config_file(config_path)

    def get(self, *args, **kwargs):
        return self.config.get(*args, **kwargs)

    def _parse_field_list_str(self, s):
        ret = None
        if s != None and len(s) > 0:
            s = s.strip()
            ret = [p.strip() for p in s.split(",")]
        return ret

    def parse_data_path_list(self,
                             section_name,
                             field_name,
                             iter=False,
                             default=None):
        ret = []
        dataPathList = self._parse_field_list_str(self.config.get(section_name, field_name))

        if iter:
            for s in dataPathList:
                ret.append(self.config.get(section_name, s))
        else:
            ret = dataPathList

        if ret == None:
            ret = default
        return ret

    def get_section_field_value(self, section_name, field_name):
        return self.config.get(section_name, field_name)

    def parse_value(self, v):
        v = str(v)
        res = v
        if v == 'None':
            res = None
        elif v in ('True', 'true'):
            res = True
        elif v in ('False', 'false'):
            res = False
        elif isFloat(v):
            res = float(v)
        elif v.isdecimal():
            res = int(v)
        return res


    def get_section_kvs(self, section_name):
        kvs = self.config.items(section_name)
        kvs = {k: self.parse_value(v) for k, v in kvs}
        return kvs


if __name__=='__main__':
    config = TaskConfig("../config/trainer.ini")

    print(config.get_section_field_value("AutoTokenizerLoader", "pretrained_model_name_or_path"))
    print(config.get_section_kvs("AutoTokenizerLoader"))
