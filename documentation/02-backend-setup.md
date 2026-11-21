# 2. Backend Setup

Run on the App EC2 instance (Amazon Linux 2023). SSH to the instance, clone
the project, then set the DB instance's private IPv4 address in
`application/backend/config.py`:

```bash
sudo dnf install -y git python3 python3-pip
git clone https://github.com/learnawsdevops/student-task-manager.git
vi ~/student-task-manager/application/backend/config.py
```

Replace `DB_PRIVATE_IP` in `config.py` with the DB instance's private IPv4
address. Then install the app:

```bash
sudo useradd --system --user-group --home /opt/taskmanager taskmanager
sudo mkdir -p /opt/taskmanager
sudo cp -r ~/student-task-manager/application /opt/taskmanager/
sudo python3 -m venv /opt/taskmanager/.venv
sudo /opt/taskmanager/.venv/bin/pip install -r /opt/taskmanager/application/backend/requirements.txt
```

Initialize the database table and install the service:

```bash
sudo -u taskmanager /opt/taskmanager/.venv/bin/python /opt/taskmanager/application/backend/init_db.py
sudo cp ~/student-task-manager/deployment/systemd/taskmanager.service /etc/systemd/system/taskmanager.service
sudo systemctl daemon-reload
sudo systemctl enable --now taskmanager
sudo systemctl status taskmanager
curl http://127.0.0.1:5000/api/health
```

The health endpoint checks that the `tasks` table and the columns used by the
API exist. `LIMIT 0` returns no task rows; it only validates the table query.
An HTTP 200 means the database is ready, while 503 means the connection,
table, or required columns are unavailable.

Gunicorn runs Flask. systemd starts it at boot and restarts it after failures.
