# 选择题
1. A (不确定，如果错了请指出)
2. B （我感觉C也行？如果是B的话，会问一嘴，但C这个应该是直接开始应用）
3. A
4. C (我感觉A也行，因为我笔记里面链接pgadmin port就是在docker run里面连接的)
5. B
6. D

# 文字题
1. 这个文件是记录资源布置，存储了资源的基础信息，可以在远程恢复吧（这段你在第一套试卷考过，但是我没记住）
2. plan是将资源部署全部罗列出来，apply是先确认是否根据plan设定资源，确定后开始实施部署
3.  
```pyhon
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}
resource "google_compute_instance" "vm" {
  count        = 5
  name         = "my-vm-${count.index + 1}"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-minimal-2210-kinetic-amd64-v20230126"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}

# Variables.tf
variable "credentials" {
  description = "My Credentials"
  default     = "./.terraform/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "nifty-structure-252803"
}

variable "region" {
  description = "Region"
  default = "us-central1-a"
}
```
4. docker-compose是跟docker-compose.yaml相关的，跑起来的话，会调动所有的services
   docker run只适用于单独调动一个service，前提条件是用系统自带的image或者已经提前装好了custom image
   如果我想调动全部service的话，会用到docker compose.  
5. 类似像下面这个command，在docker run command中加入network设定，或者可以吧所有的services全部集合到docker-compose.yaml里，这样子会自动生成一个network
```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
```
6.  
```bash
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
    networks:
      - protect_postgres

networks:
  airflow:
    external:
      name: protect_postgres

```
7.  
假设我的table里面有个field叫load_date, 可以直接用sql query
select distinct load_date
from ny_taxi
order by load_date desc
我可以看下最近哪些时间段的load_date缺失，然后返回到airflow（假设用airflow load data），查看那几天的日志
8.  
coalesce(field, defualt_value)
9. 那就检查那个时间的更新日志，看看error message怎么说的，但这个情况实在是太多了，比如数据格式不对，或者upstream变更了，或者网络不稳定等等，这个得根据情况而定，问题里面没写原因是什么，所以这里没办法展开描述
# 代码题
1.  
## main.tf
```
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "demo_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }

  iam_binding {
    role    = "roles/storage.objectViewer"
    members = ["allUsers"]
  }
}

```
## variable.tf
```
variable "credentials" {
  description = "My Credentials"
  default     = "./.terraform/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "nifty-structure-252803"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}
variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "nifty-structure-252803-terra-bucket"
}
```
（问题1：demon-bucket那个位置需要放的parameter是啥，问题2：我不知道怎么设置权限）
1.   
resource "google_compute_instance" "vm_with_docker" {
  name         = "docker-vm"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "projects/debian-cloud/global/images/debian-10-buster-v20210817"
    }
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    systemctl start docker
    systemctl enable docker
  EOT
}

2.   
```Dockerfile
FROM python:3.9

RUN pip install  --no-cache-dir pandas sqlalchemy

ENTRYPOINT ['bash']
```
4.  
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
    networks:
      - airflow
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
    network:
      - airflow
  juputernotebook:
    image: jupyter/base-notebook:latest
    volumes:
      - ./notebook:/home/docker_worker/work(这个path我不确定)    
    port:
      - "8888:8888" 
    network:
      - airflow

networks:
  airflow:
    external:
      name: airflow

sql我就不做了 我看了下大概知道思路怎么写