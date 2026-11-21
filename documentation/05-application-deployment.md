# 5. Application Deployment

Deploy in this order:

1. Follow [networking](04-networking.md) and create the three security groups.
2. Follow [database setup](01-database-setup.md).
3. Follow [backend setup](02-backend-setup.md), setting `DB_PRIVATE_IP`.
4. Follow [web setup](03-web-server-setup.md), setting `APP_PRIVATE_IP`.

Verify from your computer using the Web instance's public IP:

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
