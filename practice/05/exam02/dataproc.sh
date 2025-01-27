# 代码题第三题
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    # For my VM, it doesn't like jars config, so I commented it out
    # --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \ 
    gs://nifty-structure-252803-terra-bucket/code/process_data.py \
    -- \
        --input_green=xxx \
        --input_yellow=xxx \
        --output=xxx