# 代码题第二题
URL = 'xxx'
LOCAL_PATH = 'xxx'


mkdir -p data

wget ${URL} -O ${LOCAL_PATH}

wc ${LOCAL_PATH} >> row_count.txt

