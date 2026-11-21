# 6. Troubleshooting

## Nginx 502 Bad Gateway

```bash
# Validate Nginx syntax.
sudo nginx -t

# Check whether the Nginx service is running.
sudo systemctl status nginx

# Test the App health endpoint directly from the Web instance.
curl http://APP_PRIVATE_IP:5000/api/health

# Read the latest Nginx error log entries.
sudo tail -n 50 /var/log/nginx/error.log
```

Confirm the App private IP and TCP 5000 security group rule.

## Amazon Linux Nginx 404 page

The task-manager site should be the default server. Confirm its configuration
uses `listen 80 default_server;`, then test and reload Nginx:

```bash
# Check Nginx configuration syntax before reloading.
sudo nginx -t

# Apply the current Nginx configuration without stopping the server.
sudo systemctl reload nginx

# List files Nginx should be serving.
ls -la /var/www/taskmanager
```

## Nginx 403 Forbidden

```bash
# Check whether Nginx is running.
sudo systemctl status nginx

# List frontend files and their permissions.
sudo find /var/www/taskmanager -type f -ls

# Give Nginx ownership of the frontend files if it cannot read them.
sudo chown -R nginx:nginx /var/www/taskmanager
```

## Flask service does not start

```bash
# Check whether the Task Manager service is running.
sudo systemctl status taskmanager

# Show recent service logs, including Python or database errors.
sudo journalctl -u taskmanager -n 100 --no-pager

# Confirm the service account can run the app's Python interpreter.
sudo -u taskmanager /opt/taskmanager/.venv/bin/python --version
```

## Database connection refused

```bash
# Check whether MariaDB is listening on TCP port 3306 (run on the DB instance).
sudo ss -ltnp | grep 3306

# Check the database host configured for the App.
grep DB_HOST /opt/taskmanager/application/backend/config.py

# Check App-to-database health locally on the App instance.
curl -i http://127.0.0.1:5000/api/health
```

Check MariaDB binding, route/NACL, and DB security group.
Use the DB instance's private IPv4 address in `DB_HOST`, not its public IP,
then restart the App service:

```bash
# Restart Flask/Gunicorn after correcting the DB host or credentials.
sudo systemctl restart taskmanager
```

## Database authentication failure

Check the `Config` values in
`/opt/taskmanager/application/backend/config.py` and the App service logs:

```bash
# Show recent App logs and MariaDB grants for the app login.
sudo journalctl -u taskmanager -n 50 --no-pager
sudo mariadb -e "SHOW GRANTS FOR 'admin'@'%';"
```

## Health check logs `Unread result found`

The health check reads the zero-row query result before closing its cursor.
Deploy the latest `database.py` and restart the App service:

```bash
sudo systemctl restart taskmanager
```

## Table initialization reports CREATE denied

On the DB instance, grant `CREATE` on the application database:

```bash
# Give the app login permission to create its initial table.
sudo mariadb -e "GRANT CREATE ON taskmanager.* TO 'admin'@'%';"
```

Then rerun `init_db.py` on the App instance.

```bash
# Create the tasks table with the App's configured database connection.
sudo -u taskmanager /opt/taskmanager/.venv/bin/python /opt/taskmanager/application/backend/init_db.py
```

## Missing dependencies or disk space

```bash
# Reinstall packages listed by the backend's requirements file if missing.
sudo /opt/taskmanager/.venv/bin/pip install -r /opt/taskmanager/application/backend/requirements.txt

# Check free disk space and the size of log files.
df -h
du -sh /var/log/*
```
