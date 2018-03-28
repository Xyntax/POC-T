#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
测试用例
"""

import random
import time


def poc(str):
    return False
    time.sleep(3)
    if random.randint(1, 15) > 5:
        return True
    return False