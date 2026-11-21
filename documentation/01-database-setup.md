# 1. Database Setup

Run these commands on the DB EC2 instance (Amazon Linux 2023). SSH to the
instance, then clone the project:

```bash
sudo dnf install -y git mariadb105-server
git clone https://github.com/learnawsdevops/student-task-manager.git
sudo systemctl enable --now mariadb
sudo cp ~/student-task-manager/deployment/database/mariadb.cnf /etc/my.cnf.d/taskmanager.cnf
sudo systemctl restart mariadb
```

Create the database and application user (run once):

```bash
sudo mariadb -e "CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123'; GRANT SELECT, INSERT, UPDATE, DELETE, CREATE ON taskmanager.* TO 'admin'@'%';"
```

The app's DB user is limited to the `taskmanager` database. The training
password is `admin123`. Allow TCP 3306 only from the App security group.
Confirm MariaDB is listening with `sudo ss -ltnp | grep 3306`.
