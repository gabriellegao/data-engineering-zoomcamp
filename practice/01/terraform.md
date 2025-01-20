### Main.tf
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

resource "google_compute_instance" "default" {
  name         = "my-vm"
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
### Variables.tf
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
### Terraform Commands
After `main.tf` and `variables.tf` are ready, I cd to the location where those two files store and run the following commands
```bash
terraform init
terraform plan
terraform apply
```

### Comment
这些步骤都是在我本地操作的，如果需要在docker上操作的话，首先我得创建custom image, 其次是docker-compose.yaml

### Dockerfile
#### 使用 HashiCorp 官方提供的 Terraform 镜像
FROM hashicorp/terraform:latest

#### 设置工作目录
WORKDIR /terraform

#### 复制 Terraform 配置文件
COPY main.tf variables.tf ./

#### 复制 GCP 凭证
COPY my-creds.json /root/.google/credentials/google_credentials.json

#### 设置环境变量
ENV GOOGLE_APPLICATION_CREDENTIALS="/root/.google/credentials/google_credentials.json"

#### 运行 Terraform 初始化
ENTRYPOINT ["terraform", "apply", "-auto-approve"]


### Docker-compose.yaml
version: '3.8'
services:
  terraform:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      GOOGLE_APPLICATION_CREDENTIALS: "/root/.google/credentials/google_credentials.json"
      GCP_PROJECT_ID: "nifty-structure-252803"
    volumes:
      - ~/.google/credentials/:/root/.google/credentials:ro


### Commands
```bash
docker-compose build .
docker-compose up 
```