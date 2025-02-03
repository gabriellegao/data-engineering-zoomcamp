# https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2020-01.parquet
# https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2020-01.parquet
set -e

TAXI_TYPE=$1 #"yellow"
YEAR=$2 #2020
URL_PREFIX='https://d37ci6vzurychx.cloudfront.net/trip-data/'
for MONTH in {1..12}; do
    FMONTH=`printf "%02d" ${MONTH}`
    URL="${URL_PREFIX}${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.parquet"

    LOCAL_PREFIX="data/raw/${TAXI_TYPE}/${YEAR}/${FMONTH}"
    LOCAL_FILE="${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.parquet"
    LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

    mkdir -p ${LOCAL_PREFIX}

    echo "downloading ${URL} to local path ${LOCAL_PATH}"
    wget ${URL} -O ${LOCAL_PATH}

    gzip ${LOCAL_PATH} #unzip file
done