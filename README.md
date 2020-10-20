#todos
* actually fill out this readme
* server install scripts
* solve our database concurrency problem :(
* type hinting
* unit tests
*



## server-y notes
* general nonsense scripts
```sh
sudo systemctl status nurdbot-watcher
sudo systemctl start nurdbot-watcher
sudo systemctl stop nurdbot-watcher
sudo systemctl restart nurdbot-watcher
```
* stack driver
```sh
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
sudo bash install-logging-agent.sh
```

* python-y bits
```sh
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y
sudo apt install python3-venv -y
```

* test the stuff
```sh
git clone https://github.com/Nurdbot/nurdbot-watcher

cd nurdbot-watcher
python3 -m venv env
source env/bin/activate
pip install wheel
pip install -r requirments.txt
#test
# ! BREAK
touch config.py
#fill out your config file.
gunicorn --bind 0.0.0.0:5000 app:app
deactivate
cd ..
```
* create a service file
```sh
sudo nano /etc/systemd/system/nurdbot-watcher.service

[Unit]
Description=Gunicorn instance to serve nurdbot-watcher
After=network.target

[Service]
User=jay
Group=www-data
#this can be whatever
WorkingDirectory=/home/jay/nurdbot-watcher
Environment="PATH=/home/jay/nurdbot-watcher/env/bin"
ExecStart=/home/jay/nurdbot-watcher/env/bin/gunicorn --workers 3 --bind unix:nurdbot-watcher.sock -m 007 app:app
#/end can be whatever
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
* install le service
```sh
sudo systemctl start nurdbot-watcher
sudo systemctl enable nurdbot-watcher
sudo systemctl status nurdbot-watcher
```
* nginx-y bits
```sh
sudo apt install nginx
```
```sh
sudo nano /etc/nginx/sites-available/nurdbot-watcher
#paste this
server {
    listen 80;
    server_name watcher.nurdbot.dev www.watcher.nurdbot.dev;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/jay/nurdbot-watcher/nurdbot-watcher.sock;
    }
}
```
```sh
sudo ln -s /etc/nginx/sites-available/nurdbot-watcher /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```
* ssl
```
sudo apt install python-certbot-nginx
sudo certbot --nginx -d watcher.nurdbot.dev
``` 