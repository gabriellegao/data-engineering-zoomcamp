'''
Shell 命令与错误处理 编写一个 Shell 脚本，完成以下任务：

下载纽约出租车数据（URL 可参数化传入）。
使用 gzip 解压文件。
如果解压成功，统计文件行数并打印到控制台。
如果失败，记录错误日志到 error.log。
'''
set -e

URL = $1

LOCAL_PATH = "pth/to/folder"
LOCAL_FILE = "${LOCAL_PATH}/my_file.csv"

wget -O ${LOCAL_FILE} ${URL}
gzip ${LOCAL_FILE}

if [-s ${LOCAL_FILE}]; then
    echo "wc -l ${LOCAL_FILE} | awk '{print $2}'"
else 
    echo $? > error.log