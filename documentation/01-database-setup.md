# 1. Database Setup

Run these commands on the DB EC2 instance with Amazon Linux 2023.
Create the database and application user once; the backend initialization
script creates the table using the app user's limited database permissions.

```bash
sudo dnf install -y mariadb105-server
sudo systemctl enable --now mariadb
sudo mysql_secure_installation
sudo mariadb -u root -p
```

Create the database and application user:

```sql
CREATE DATABASE taskmanager \
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; \
CREATE USER 'admin'@'%' \
  IDENTIFIED BY 'admin123'; \
GRANT SELECT, INSERT, UPDATE, DELETE ON taskmanager.* \
  TO 'admin'@'%'; \
FLUSH PRIVILEGES; \
EXIT;
```

Use the constant training password `admin123`. Restrict network access
with the AWS DB security group instead of adding an application-subnet
dependency.

Copy and verify:

```bash
sudo cp deployment/database/mariadb.cnf /etc/my.cnf.d/taskmanager.cnf
sudo systemctl restart mariadb
sudo ss -ltnp | grep 3306
mysql -h 127.0.0.1 -u admin -padmin123 taskmanager
```

Allow port 3306 only from the App security group.
