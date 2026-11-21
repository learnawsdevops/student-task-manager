# Student Task Manager

A beginner-friendly, three-tier task application for AWS EC2 practice.

## Architecture

- **Web tier:** EC2 with Nginx on port 80; serves the frontend and proxies `/api/` to the app tier.
- **App tier:** EC2 with Flask and Gunicorn on port 5000.
- **Database tier:** EC2 with MariaDB on port 3306.

For this training setup, all three instances have public IPs so trainees can
SSH directly to them. Security groups restrict SSH to the trainee's IP and
allow application traffic only between tiers. App and DB ports are not open
to the internet.

## Repository

- `application/frontend/` – HTML, CSS and JavaScript
- `application/backend/` – Flask API, MariaDB helpers and initialization
- `deployment/nginx/` – Nginx configuration
- `deployment/systemd/` – Gunicorn systemd service
- `deployment/database/` – MariaDB configuration
- `documentation/` – setup and troubleshooting guides

## Deployment

1. Launch three Amazon Linux 2023 EC2 instances in the same public subnet of the default VPC, with auto-assigned public IPv4 addresses.
2. Create the security group rules in [networking](documentation/04-networking.md).
3. Follow [database setup](documentation/01-database-setup.md), then [backend setup](documentation/02-backend-setup.md), then [web setup](documentation/03-web-server-setup.md).
4. Open `http://<web-public-ip>/`.

The only application settings to change are the DB private IP in
`application/backend/config.py` and the App private IP in the Nginx config.
The `admin` / `admin123` credentials are for this training project only; do
not use them in production.
