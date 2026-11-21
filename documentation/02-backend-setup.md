# 2. Backend Setup

Run on the App EC2 instance.

```bash
sudo dnf install -y python3 python3-pip
sudo useradd --system --home /opt/taskmanager taskmanager
sudo mkdir -p /opt/taskmanager
sudo cp -r application /opt/taskmanager/
sudo python3 -m venv /opt/taskmanager/.venv
sudo /opt/taskmanager/.venv/bin/pip install -r /opt/taskmanager/application/backend/requirements.txt
```

Create `/etc/taskmanager/taskmanager.env`:

```bash
sudo mkdir -p /etc/taskmanager
sudo chmod 700 /etc/taskmanager
sudo vi /etc/taskmanager/taskmanager.env
```

Copy `application/.env.example` to `/etc/taskmanager/taskmanager.env`.
Set `DB_HOST` to the database server's private IP address. Use
`admin123` as `DB_PASSWORD`; the remaining values are already
configured for this training application.

Initialize the table:

```bash
cd /opt/taskmanager/application/backend
set -a
source /etc/taskmanager/taskmanager.env
set +a
/opt/taskmanager/.venv/bin/python init_db.py
```

Install the service:

```bash
sudo cp /path/to/taskmanager.service /etc/systemd/system/taskmanager.service
sudo systemctl daemon-reload
sudo systemctl enable --now taskmanager
sudo systemctl status taskmanager
curl http://127.0.0.1:5000/api/health
```

Gunicorn runs Flask. systemd starts it at boot and restarts it after failures.
