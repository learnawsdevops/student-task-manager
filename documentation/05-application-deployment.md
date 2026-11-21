# 5. Application Deployment

Deploy one tier at a time in this order. Each linked guide gives the commands
for that instance and explains their purpose:

1. Follow [networking](04-networking.md) and attach the tier-specific security groups.
2. Follow [database setup](01-database-setup.md) to start MariaDB and create its database and user.
3. Follow [backend setup](02-backend-setup.md), setting `DB_PRIVATE_IP`, to create the table and start Flask/Gunicorn.
4. Follow [web setup](03-web-server-setup.md), setting `APP_PRIVATE_IP`, to serve the frontend and proxy API requests.

Verify from your computer using the Web instance's public IP:

```bash
# Confirm the API and database health through the Web tier.
curl http://<web-ip>/api/health

# List tasks currently stored in the database.
curl http://<web-ip>/api/tasks

# Create a task and print the new task returned by the API.
curl -X POST http://<web-ip>/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Study networking"}'

# Mark task 1 complete; use the ID returned by the POST if it differs.
curl -X PATCH http://<web-ip>/api/tasks/1 \
  -H 'Content-Type: application/json' \
  -d '{"completed":true}'

# Delete that task using its ID.
curl -X DELETE http://<web-ip>/api/tasks/1
```
