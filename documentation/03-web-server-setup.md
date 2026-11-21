# 3. Web Server Setup

Run on the Web EC2 instance (Amazon Linux 2023). SSH to the instance, clone
the project, and set the App instance's private IPv4 address in the Nginx
config:

```bash
sudo dnf install -y git nginx
git clone https://github.com/learnawsdevops/student-task-manager.git
vi ~/student-task-manager/deployment/nginx/taskmanager.conf
```

Replace `APP_PRIVATE_IP` in `taskmanager.conf` with the App instance's
private IPv4 address. Then install and start Nginx:

```bash
sudo mkdir -p /var/www/taskmanager
sudo cp -r ~/student-task-manager/application/frontend/. /var/www/taskmanager/
sudo cp ~/student-task-manager/deployment/nginx/taskmanager.conf /etc/nginx/conf.d/taskmanager.conf
sudo nginx -t
sudo systemctl enable --now nginx
curl http://localhost/api/health
```

Open `http://<web-public-ip>/`.
