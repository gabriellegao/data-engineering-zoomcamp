## Setup SSH
### Create .ssh folder
```bash
mkdir ~/.ssh
```

### Create SSH keys for google cloud
Return two keys: gcp (private key) and gcp.pub (public key)  
Public key to lock the VM, and privaye key to unlock the VM 
```bash
ssh-keygen -t rsa -f ~/.ssh/gcp -C gabrielle -b 2048 
``` 

### Upload the SSH key to Metadata under Compute Engine
Paste the output in SSH Keys box to lock VM
```bash
cat gcp.pub
```

### Connect SSH and VM
Unlock the VM on your local machine
```bash
ssh -i ~/.ssh/gcp gabrielle@<external_ip_address>
```

### Create Config File
```bash
cd ~/.ssh
touch config
```

### Config File
```bash
Host <ssh-name>
    HostName <external_ip_address>
    User gabrielle
    IdentityFile ~/.ssh/gcp
```

## Install Packages
### Install Anaconda
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh 
bash Anaconda3-2021.11-Linux-x86_64.sh
```
### Apply Changes in `.bashrc`
这个command的作用在于，让当前终端重新加载`.bashrc`文件内的所有设置，无需关闭或者重启终端  
```bash
source .bashrc
```


### Login to SSH
```bash
ssh de-zoocamp
```

### Logout from SSH
```bash
ctrl + D
#or
type logout
```

### Shut Down SSH
```bash
sudo shutdown now
```

### Download Docker
```bash
sudo apt-get update
sudo apt-get install docker.io
```
The following command allows us to run docker without `sudo`
```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
logout #Logout and login back again will aplly the changes we made
ssh de-zoomcamp
```
### Download Docker Compose
To organize executable files, you can create a `bin` folder and place docker-compose package inside
```bash
mkdir bin
cd bin/
```
Download and rename the docker-compose file
```bash
wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
```
Make the file executable
```bash
chmod +x docker-compose
```

### Add command in .bashrc file
1. 这个指令的好处在于，将bin下面可执行的包全部加入到PATH里，以后运行这些包就不需要cd到它存储的位置了
2. 在添加完export指令后，跑source .bashrc可以刷新.bashrc file，使更改立即生效
3. 更改完后，`ctrl + O`存储更改，`Enter`确认文件名，`ctrl + X`退出文件

```bash
nano/vim .bashrc
export PATH="${HOME}/bin:${PATH}"
source .bashrc
```

### Fix Error for Pgcopg Import Issue
```bash
sudo apt-get install python-dev libpq-dev libevent-dev
pip install pgcli
```

## Google Cloud CLI and Terraform
### Google CLoud CLI Setup
- Move credential json file from local machine to google cloud
```bash
cd ~/.google/credentials/ # Locate the json file
sftp de-zoomcamp # Connect to Google VM
mkdir ~/.google/credentials/
put google_credentials.json # Upload json file to cloud
```
- Assign the service account private key (`.json`) to `GOOGLE_APPLICATION_CREDENTIALS`
- Add command to `.bashrc`
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.google/credentials/google_credentials.json
```
- Authenticate and connect to service account with credential
```bash
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```
### Terraform Setup
Go to location whhere `main.tf` and `variables.tf` store
```bash
# Initialize terraform
terraform init
```
Generate exectution plan
```bash
terraform plan
```
Execute plan, applying changes and modify infrastructure
```bash
terraform apply
```

### Port
在ssh上启动了docker compose, 并且把port添加至vscode port界面，使port映射到localhost,那么在本地docker compose休眠或关闭状态，也可连接到ssh的docker compose中的postgres and pgAdmin. 

## Setup Google Cloud SDK
### Install SDK Package
```bash
mkdir .gcloud
# Install
wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-x86_64.tar.gz google-cloud-cli-darwin-x86_64.tar.gz 
# Unpack
tar xzfv google-cloud-cli-darwin-x86_64.tar.gz
# Remove Installer
rm google-cloud-cli-darwin-x86_64.tar.gz
```

### Initialize SDK
```bash
# Run installation script
./google-cloud-sdk/install.sh
# Initialize gcloud
./google-cloud-sdk/bin/gcloud init
```

### Add Gcloud to PATH
```bash
nano .zshrc
export CLOUD_SDK_HOME="${HOME}/.gcloud/google-cloud-sdk"
export PATH="${CLOUD_SDK_HOME}/bin:${PATH}"
source .zshrc
```

### Start VM Remotely
```bash
gcloud compute instances start de-zoomcamp --zone=<ZONE>
```

## Additional Notes
### Terraform: `count.index`
```h
resource "google_compute_instance" "vm" {
  count = 3
  name  = "my-vm-${count.index + 1}"
}
```
- `vm`: define internal name of this virtual machine.  
- `count.index`: subfix of instance, `my-vm-0`, `my-vm-1` and `my-vm-2`.  
- `name=`: specify external name of this instance
### Terraform: `for_each`
`for_each` has the same function as `count`.
```h
resource "google_compute_instance" "vm" {
  for_each = toset(["vm-1", "vm-2", "vm-3"])
  name     = each.key
}
```
### Terraform: `metadata-startup_script`
```h
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
```
### Terraform Commands
```bash
# 管理状态文件
terraform backend
# 导入部署资源信息
terraform import
```