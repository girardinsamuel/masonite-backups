"""Backups Settings"""
from masonite.environment import env

BACKUP = {
    "name": env("APP_NAME", "masonite-project"),
    "source": {
        "files": [],
        "databases": [],
    },
    "destination": {
        "disks": []
    }
}
