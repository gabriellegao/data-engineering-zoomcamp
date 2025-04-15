## Docker Basics
### Build Image 
In default, Docker only looks for the file named `Dockerfile`
```docker
docker build -t <image_name> .
```

### Create Container
Create a new container based on the image
```docker
docker run -it \
  <--entrypoint=> \
  <--name=optional:container_name> \
  <image_name> <**kwarg>
```

### Execute Container
Open and enter the bash shell in existing container
```docker
docker exec -it <container_name> bash
```

### List All Running Containers
```bash
docker ps
```
### List All Containers
```bash
docker ps -a
```
## Connect Docker to Postgres and PgAdmin
### Connect to Postgres
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

### Connect to PgAdmin
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

### *Attention*
*Postgres and PgAdmin live in different containers after running two commands above. They are isolated and aren't able to communicate with each others.*  
*To build connection between Postgres and PgAdmin, we need to use `Docker Network`*

### Login to Postgres (Outside of docker)
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

### Login to Postgres (Inside of docker)
```bash
pgcli -h pgdatabase -p 5432 -u root -d ny_taxi
```
## Docker Network
### Why Docker Network?
Docker network benefits communications among inside container. 
- `bridge`: 多个容器在同一个 Docker 主机上相互通信，但又与外部网络隔离
- `hotst`: 容器与主机的网络环境无隔离
### Create Docker Netwowrk
```bash
docker network create pg-network
```

### Run Postgress in Network
- Create a container upon the image `postgres:13`, and set the user name and password for identity verification.   
- Host `pg-database`看守着 port `5432`这个门，任何想要进入`5432`的行为，都需要先通过身份验证
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name=pg-database \
  postgres:13
```

### Run PgAdmin in Network
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

### Convert Jupyter notebook to Python Script
```bash
jupyter nbconvert --to=script upload-data.ipynb
```

### Upload Data with Python Script
- Download data from URL
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```
- Run python script with args
- Upload data to Postgres from local machine
```bash
python ingest_data.py \
# Read the args from below and put them into ingest_data.py
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```
## Docker Network + Docker Custom Image
### Build Docker Custom Image
- 先创建好一个image连接着预设好的dockerfile, 包括环境以及python script.
- In default, docker only looks for the file named `Dockerfile` to build the image.
```bash
docker build -t taxi_ingest:v001 .
```  
### Download Data from URL
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```
### Prepare Arguments in `ingest_data.py`
```python
import argparse

parser = argparse.ArgumentParser(description='Ingest CSV data to Postgress')

parser.add_argument('--user', help = 'user name')
parser.add_argument('--password', help = 'password')
parser.add_argument('--host', help = 'host')
parser.add_argument('--port', help = 'port')
parser.add_argument('--db', help = 'database name')
parser.add_argument('--table_name', help ='table name')
parser.add_argument('--url', help = 'csv url')

args = parser.parse_args()
```
### Run Docker Container
- `taxi_ingest:v001`是image, 这段代码的作用在于，借用image的设定创建一个container，并将这个container加入到pg-network网络里，在pg-database里已经设定好了user name and password. 当我们需要读取5432后面的数据时，需要找到其对应的host(看门人)以及port(门牌号)。再用user name and password解锁。
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
## Docker Compose
### Run docker compose (Live, monitor logs)
```bash
docker-compose up
```
### Run docker compose (Background)
```bash
docker-compose up -d
```

### Shut down docker compose
```bash
docker-compose down
```
