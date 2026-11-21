# 1. Database Setup

Run each command on the DB EC2 instance (Amazon Linux 2023). The commands
install MariaDB, download the project files, and configure MariaDB to accept
connections from the App instance:

```bash
# Install Git (to download the project) and the MariaDB server.
sudo dnf install -y git mariadb105-server

# Download the full repository, which contains the database configuration.
git clone https://github.com/learnawsdevops/student-task-manager.git

# Start MariaDB now and start it automatically after a reboot.
sudo systemctl enable --now mariadb

# Install the project's MariaDB network-listener configuration.
sudo cp ~/student-task-manager/deployment/database/mariadb.cnf /etc/my.cnf.d/taskmanager.cnf

# Restart MariaDB so it reads the new configuration.
sudo systemctl restart mariadb
```

Create the database and application user (run once). `sudo mariadb -e` opens
the MariaDB command-line client as the local administrator, runs the SQL
statements, and exits:

```bash
sudo mariadb -e "
CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE ON taskmanager.* TO 'admin'@'%';
"
```

The SQL statements create the database, create the app login, then grant that
login permission to create the table and read/write tasks in `taskmanager`.
The training password is `admin123`.

In the DB security group, allow TCP port 3306 only from the App security
group. Confirm MariaDB is listening on that port:

```bash
# List listening TCP sockets and filter for MariaDB's port, 3306.
sudo ss -ltnp | grep 3306
```
