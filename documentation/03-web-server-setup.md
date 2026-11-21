# 3. Web Server Setup

Run on the Web EC2 instance.

```bash
sudo dnf install -y nginx
sudo mkdir -p /var/www/taskmanager
sudo cp -r application/frontend/* /var/www/taskmanager/
sudo vi deployment/nginx/taskmanager.conf
```

Replace `10.0.2.20` with the App EC2 private IP, then install:

```bash
sudo cp deployment/nginx/taskmanager.conf /etc/nginx/conf.d/taskmanager.conf
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
curl http://localhost/api/health
```

Open `http://<web-public-ip>/`.
