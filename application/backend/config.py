"""Training deployment settings. Replace DB_PRIVATE_IP before deployment."""


class Config:
    DB_HOST = "DB_PRIVATE_IP"
    DB_PORT = 3306
    DB_NAME = "taskmanager"
    DB_USER = "admin"
    DB_PASSWORD = "admin123"

