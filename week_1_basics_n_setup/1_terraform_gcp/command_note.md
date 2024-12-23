# Creat .ssh folder
mkdir ~/.ssh

# Create SSH keys for google cloud
ssh-keygen -t rsa -f ~/.ssh/gcp -C gabrielle -b 2048
--> return two keys: gcp (private key) and gcp.pub (public key) 
--> public key to lock the VM, and privaye key to unlock the VM

# Upload the SSH key to Metadata under Compute Engine
cat gcp.pub
--> paste the output in SSH Keys box
--> to lock the VM

# Connect SSH and VM
ssh -i ~/.ssh/gcp gabrielle@<external_ip_address>
--> unlock the VM on your local machine

# Create Config File
cd ~/.ssh
touch config

# Config File
Host <ssh-name>
    HostName <external_ip_address>
    User gabrielle
    IdentityFile ~/.ssh/gcp

# Login to SSH
ssh de-zoocamp
or
source .bashrc

# Logout from SSH
ctrl + D
or
type logout

# Download Docker
sudo apt-get install docker.io

# Add command in .bashrc file
nano/vim .bashrc
export PATH="${HOME}/bin:${PATH}"
source .bashrc
--> 这个指令的好处在于，将bin下面可执行的包全部加入到PATH里，以后运行这些包就不需要cd到它存储的位置了
--> 在添加完export指令后，跑source .bashrc可以刷新.bashrc file，使更改立即生效

# To fixed error for pgcopg import issue
sudo apt-get install python-dev libpq-dev libevent-dev
pip install pgcli

# Google Cloud CLI
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/my-creds.json

# Port
## 在ssh上启动了docker compose, 并且把port添加至vscode port界面，使port映射到localhost,那么在本地docker compose休眠或关闭状态，也可链接docker compose中的postgres and pgAdmin. 