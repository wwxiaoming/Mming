#!/usr/bin/env python3
"""生成批量URL列表，供curl批量下载"""

import os

# 清除代理设置
for k in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    os.environ.pop(k, None)

def generate_all_batches():
    """生成所有批次的URL和输出文件名"""
    batches = []
    
    # 沪市 600000-605999
    for start in range(600000, 606000, 50):
        end = min(start + 49, 605999)
        codes = ','.join([f'sh{i}' for i in range(start, end + 1)])
        url = f'https://qt.gtimg.cn/q={codes}'
        outfile = f'/workspace/raw_data/sh_{start}_{end}.txt'
        batches.append((url, outfile))
    
    # 深市 000001-004999
    for start in range(1, 5000, 50):
        end = min(start + 49, 4999)
        codes = ','.join([f'sz{i:06d}' for i in range(start, end + 1)])
        url = f'https://qt.gtimg.cn/q={codes}'
        outfile = f'/workspace/raw_data/sz_{start}_{end}.txt'
        batches.append((url, outfile))
    
    # 创业板 300001-301999
    for start in range(300001, 302000, 50):
        end = min(start + 49, 301999)
        codes = ','.join([f'sz{i}' for i in range(start, end + 1)])
        url = f'https://qt.gtimg.cn/q={codes}'
        outfile = f'/workspace/raw_data/cy_{start}_{end}.txt'
        batches.append((url, outfile))
    
    return batches

def main():
    os.makedirs('/workspace/raw_data', exist_ok=True)
    batches = generate_all_batches()
    
    # 写入URL列表文件
    with open('/workspace/url_list.txt', 'w') as f:
        for url, outfile in batches:
            f.write(f'{url}\t{outfile}\n')
    
    print(f'共 {len(batches)} 个批次')
    print('URL列表已保存到 /workspace/url_list.txt')

if __name__ == '__main__':
    main()
