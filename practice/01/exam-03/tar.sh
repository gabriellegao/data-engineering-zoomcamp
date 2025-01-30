tar -zcvf logs_backup.tar.gz /path/to/dir/

file_size = ls -lh logs_backup.tar.gz

echo "${file_size}"



#!/bin/bash

# 压缩 .log 文件
tar -zcvf logs_backup.tar.gz *.log

# 输出压缩文件大小
# awk: 自动解析seperator, $5 print 5th column in each row
file_size=$(ls -lh logs_backup.tar.gz | awk '{print $5}')
echo "Backup size: $file_size"
