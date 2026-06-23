# -*- coding: utf-8 -*-
"""探索可用的akshare接口"""
import akshare as ak
import warnings
warnings.filterwarnings('ignore')

# 列出akshare中含"minute"或"trend"的函数
funcs = [f for f in dir(ak) if 'minute' in f.lower() or 'trend' in f.lower() or 'spot' in f.lower() or 'index' in f.lower()]
print("含minute/trend/spot/index的函数:")
for f in funcs:
    print(f"  - ak.{f}")
