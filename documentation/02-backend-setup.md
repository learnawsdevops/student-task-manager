# 2. Backend Setup

Run on the App EC2 instance (Amazon Linux 2023). Install the tools, download
the project, and open the backend configuration:

```bash
# Install Git, Python, and pip.
sudo dnf install -y git python3 python3-pip

# Download the application source code and deployment files.
git clone https://github.com/learnawsdevops/student-task-manager.git

# Open the backend configuration to set the DB's private IP.
vi ~/student-task-manager/application/backend/config.py
```

Replace `DB_PRIVATE_IP` in `config.py` with the DB instance's private IPv4
address. The other values are the training database name and credentials.
Then create the service account and install the app:

```bash
# Create a non-login system user and matching group for the app service.
sudo useradd --system --user-group --home /opt/taskmanager taskmanager

# Create the directory where the application will run.
sudo mkdir -p /opt/taskmanager

# Copy the application source to its runtime location.
sudo cp -r ~/student-task-manager/application /opt/taskmanager/

# Create an isolated Python environment for this application.
sudo python3 -m venv /opt/taskmanager/.venv

# Install Flask, Gunicorn, and the MySQL connector into that environment.
sudo /opt/taskmanager/.venv/bin/pip install -r /opt/taskmanager/application/backend/requirements.txt
```

Initialize the database table, install the systemd service definition, and
start the service:

```bash
# Create the tasks table using the app's configured DB connection.
sudo -u taskmanager /opt/taskmanager/.venv/bin/python /opt/taskmanager/application/backend/init_db.py

# Install the service definition that tells systemd how to run Gunicorn.
sudo cp ~/student-task-manager/deployment/systemd/taskmanager.service /etc/systemd/system/taskmanager.service

# Make systemd reload its service definitions.
sudo systemctl daemon-reload

# Enable the service at boot and start it immediately.
sudo systemctl enable --now taskmanager

# Show whether the service is running.
sudo systemctl status taskmanager

# Check the App API and database health locally on this instance.
curl http://127.0.0.1:5000/api/health
```

The health endpoint checks that the `tasks` table and the columns used by the
API exist. `LIMIT 0` returns no task rows; it only validates the table query.
An HTTP 200 means the database is ready, while 503 means the connection,
table, or required columns are unavailable.

Gunicorn runs Flask. systemd starts it at boot and restarts it after failures.
