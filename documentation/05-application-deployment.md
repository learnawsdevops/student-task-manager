# 5. Application Deployment

Deploy in this order:

1. Create database and app security groups.
2. Install and configure MariaDB on the DB instance.
3. Copy backend files and install Python dependencies on the App instance.
4. Add `/etc/taskmanager/taskmanager.env`.
5. Run `init_db.py`.
6. Install and start the systemd service.
7. Deploy frontend files to Nginx on the Web instance.
8. Replace the App private IP placeholder in Nginx.
9. Validate and reload Nginx.

Verification:

```bash
curl http://<web-ip>/api/health
curl http://<web-ip>/api/tasks
curl -X POST http://<web-ip>/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Study networking"}'
curl -X PATCH http://<web-ip>/api/tasks/1 \
  -H 'Content-Type: application/json' \
  -d '{"completed":true}'
curl -X DELETE http://<web-ip>/api/tasks/1
```
