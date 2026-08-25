from pathlib import Path
import os
import sys

import django
from django.test import Client

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)

    response = Client(HTTP_HOST="localhost").get("/")
    if response.status_code != 200:
        raise SystemExit(f"No se pudo renderizar la pagina principal: {response.status_code}")

    (public_dir / "index.html").write_bytes(response.content)


if __name__ == "__main__":
    main()
