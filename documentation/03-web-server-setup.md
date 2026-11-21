# 3. Web Server Setup

Run on the Web EC2 instance (Amazon Linux 2023). Install Git and Nginx,
download the project files, and open the Nginx configuration:

```bash
# Install Git and the Nginx web server.
sudo dnf install -y git nginx

# Download the frontend and Nginx configuration.
git clone https://github.com/learnawsdevops/student-task-manager.git

# Open the Nginx configuration to set the App's private IP.
vi ~/student-task-manager/deployment/nginx/taskmanager.conf
```

Replace `APP_PRIVATE_IP` in `taskmanager.conf` with the App instance's
private IPv4 address. Then install the frontend and Nginx configuration:

```bash
# Create the directory from which Nginx will serve the frontend.
sudo mkdir -p /var/www/taskmanager

# Copy the frontend files into Nginx's document root.
sudo cp -r ~/student-task-manager/application/frontend/. /var/www/taskmanager/

# Install the Nginx site configuration.
sudo cp ~/student-task-manager/deployment/nginx/taskmanager.conf /etc/nginx/conf.d/taskmanager.conf

# Check Nginx configuration syntax before applying it.
sudo nginx -t

# Enable Nginx at boot and start it now.
sudo systemctl enable --now nginx

# Reload Nginx to apply the site configuration.
sudo systemctl reload nginx
```

Open `http://<web-public-ip>/` in a browser to load the frontend. The frontend
uses `/api/` requests, which Nginx forwards to the App instance.
