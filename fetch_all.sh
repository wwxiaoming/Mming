#!/bin/bash
# 批量获取A股行情数据并保存到文件
# 用法: bash fetch_all.sh

set -e

OUTDIR="/workspace/raw_data"
mkdir -p "$OUTDIR"

# 沪市 600000-605999
for start in $(seq 600000 50 605950); do
    end=$((start + 49))
    if [ $end -gt 605999 ]; then end=605999; fi
    
    codes=""
    for i in $(seq $start $end); do
        if [ -z "$codes" ]; then
            codes="sh$i"
        else
            codes="$codes,sh$i"
        fi
    done
    
    url="https://qt.gtimg.cn/q=$codes"
    outfile="$OUTDIR/sh_${start}_${end}.txt"
    
    curl -s --connect-timeout 10 --max-time 15 "$url" -o "$outfile" 2>/dev/null || true
    echo "Fetched sh $start-$end, size=$(wc -c < "$outfile" 2>/dev/null || echo 0)"
    
    sleep 0.3
done

# 深市 000001-004999
for start in $(seq 1 50 4999); do
    end=$((start + 49))
    if [ $end -gt 4999 ]; then end=4999; fi
    
    codes=""
    for i in $(seq $start $end); do
        code=$(printf "%06d" $i)
        if [ -z "$codes" ]; then
            codes="sz$code"
        else
            codes="$codes,sz$code"
        fi
    done
    
    url="https://qt.gtimg.cn/q=$codes"
    outfile="$OUTDIR/sz_${start}_${end}.txt"
    
    curl -s --connect-timeout 10 --max-time 15 "$url" -o "$outfile" 2>/dev/null || true
    echo "Fetched sz $start-$end, size=$(wc -c < "$outfile" 2>/dev/null || echo 0)"
    
    sleep 0.3
done

# 创业板 300001-301999
for start in $(seq 300001 50 301999); do
    end=$((start + 49))
    if [ $end -gt 301999 ]; then end=301999; fi
    
    codes=""
    for i in $(seq $start $end); do
        if [ -z "$codes" ]; then
            codes="sz$i"
        else
            codes="$codes,sz$i"
        fi
    done
    
    url="https://qt.gtimg.cn/q=$codes"
    outfile="$OUTDIR/cy_${start}_${end}.txt"
    
    curl -s --connect-timeout 10 --max-time 15 "$url" -o "$outfile" 2>/dev/null || true
    echo "Fetched cy $start-$end, size=$(wc -c < "$outfile" 2>/dev/null || echo 0)"
    
    sleep 0.3
done

echo "All data fetched!"
