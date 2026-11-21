# 6. Troubleshooting

## Nginx 502 Bad Gateway

```bash
sudo nginx -t
sudo systemctl status nginx
curl http://<app-private-ip>:5000/api/health
sudo tail -n 50 /var/log/nginx/error.log
```

Confirm the App private IP and TCP 5000 security group rule.

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
mysql -h <db-private-ip> -u admin -p taskmanager
```

Check MariaDB binding, route/NACL, and DB security group.

## Database authentication failure

Check `.env` values and the SQL-created username/host. Reopen MariaDB and verify:

```sql
SELECT User, Host FROM mysql.user;
SHOW GRANTS FOR 'admin'@'%';
```

## Missing dependencies or disk space

```bash
sudo /opt/taskmanager/.venv/bin/pip install -r /opt/taskmanager/application/backend/requirements.txt
df -h
du -sh /var/log/*
```
