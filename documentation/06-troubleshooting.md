# 6. Troubleshooting

## Nginx 502 Bad Gateway

```bash
sudo nginx -t
sudo systemctl status nginx
curl http://APP_PRIVATE_IP:5000/api/health
sudo tail -n 50 /var/log/nginx/error.log
```

Confirm the App private IP and TCP 5000 security group rule.

## Amazon Linux Nginx 404 page

The task-manager site should be the default server. Confirm its configuration
uses `listen 80 default_server;`, then test and reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
ls -la /var/www/taskmanager
```

## Nginx 403 Forbidden

```bash
sudo systemctl status nginx
sudo find /var/www/taskmanager -type f -ls
sudo chown -R nginx:nginx /var/www/taskmanager
```

## Flask service does not start

```bash
sudo systemctl status taskmanager
sudo journalctl -u taskmanager -n 100 --no-pager
sudo -u taskmanager /opt/taskmanager/.venv/bin/python --version
```

## Database connection refused

```bash
sudo ss -ltnp | grep 3306
grep DB_HOST /opt/taskmanager/application/backend/config.py
curl -i http://127.0.0.1:5000/api/health
```

Check MariaDB binding, route/NACL, and DB security group.
Use the DB instance's private IPv4 address in `DB_HOST`, not its public IP,
then restart the App service:

```bash
sudo systemctl restart taskmanager
```

## Database authentication failure

Check the `Config` values in
`/opt/taskmanager/application/backend/config.py` and the App service logs:

```bash
sudo journalctl -u taskmanager -n 50 --no-pager
sudo mariadb -e "SHOW GRANTS FOR 'admin'@'%';"
```

## Table initialization reports CREATE denied

On the DB instance, grant `CREATE` on the application database:

```bash
sudo mariadb -e "GRANT CREATE ON taskmanager.* TO 'admin'@'%';"
```

Then rerun `init_db.py` on the App instance.

## Missing dependencies or disk space

```bash
sudo /opt/taskmanager/.venv/bin/pip install -r /opt/taskmanager/application/backend/requirements.txt
df -h
du -sh /var/log/*
```
