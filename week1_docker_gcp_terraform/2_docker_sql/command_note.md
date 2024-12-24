# Build image 
docker build -t <image_name> .
--> In default, Docker only looks for the file named Dockerfile

# Run image 
docker run -it <container_name>

# Check the running containers
docker ps

# Check all the containers
docker ps -a

# Connection to Postgres
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

# Connection to PgAdmin
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4

# Login to Postgres
pgcli -h localhost -p 5432 -u root -d ny_taxi

# Create netwowrk
docker network create pg-network

# Run Postgress in network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
--> Create a container upon the image postgres:13, and set the user name and password for identity verification. pg-database看守着5432这个门，任何想要进入5432的行为，都需要先通过身份验证

# Run PgAdmin in network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4

# Convert Jupyter notebook to python script
jupyter nbconvert --to=script upload-data.ipynb

# Upload data using py script
```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```
```bash
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```
# Run docker
```docker build -t taxi_ingest:v001 .```
--> 先创建好一个image连接着预设好的dockerfile, 包括环境以及script
--> In default, docker only look for the file named Dockerfile to build the image

```URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"```

```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

--> taxi_ingest:v001是image, 这段代码的作用在于，借用image的设定创建一个container，并将这个container加入到pg-network网络里，在pg-database里已经设定好了user name and password. 当我们需要读取5432后面的数据时，需要找到其对应的host（看门人）以及port（门牌号）。再用user name and password解锁。

# Run docker compose (Live, monitor logs)
```bash
docker-compose up
```
# Run docker compose (Background)
docker-compose up -d

# Shut down docker compose
docker-compose down
