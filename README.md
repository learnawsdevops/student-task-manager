# Student Task Manager

A beginner-friendly, three-tier task application for AWS EC2 practice.

## Architecture

- **Web tier:** EC2 with Nginx on port 80; serves the frontend and proxies `/api/` to the app tier.
- **App tier:** EC2 with Flask and Gunicorn on private port 5000.
- **Database tier:** EC2 with MariaDB on private port 3306.

The app tier and database tier must not have public IP addresses.

## Repository

- `application/frontend/` – HTML, CSS and JavaScript
- `application/backend/` – Flask API, MariaDB helpers and initialization
- `deployment/nginx/` – Nginx configuration
- `deployment/systemd/` – Gunicorn systemd service
- `deployment/database/` – MariaDB configuration
- `documentation/` – setup and troubleshooting guides

## Quick start

1. Follow [database setup](documentation/01-database-setup.md).
2. Follow [backend setup](documentation/02-backend-setup.md).
3. Follow [web setup](documentation/03-web-server-setup.md).
4. Open `http://<web-public-ip>/`.

Backend environment variables are documented in `application/.env.example`.
