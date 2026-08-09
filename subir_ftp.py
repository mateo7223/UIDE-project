import os
from ftplib import FTP, FTP_TLS, error_perm
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

EXCLUIR = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".env",
    "db.sqlite3",
    "staticfiles",
}


class FTP_TLS_SesionReutilizable(FTP_TLS):
    """FTPS compatible con servidores que exigen reanudar la sesión TLS."""

    def ntransfercmd(self, cmd, rest=None):
        # FTP.ntransfercmd crea el socket de datos sin envolverlo en TLS.
        conexion, tamano = FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conexion = self.context.wrap_socket(
                conexion,
                server_hostname=self.host,
                session=self.sock.session,
            )
        return conexion, tamano


def asegurar_directorio(ftp, ruta):
    partes = [p for p in ruta.replace("\\", "/").split("/") if p]

    if ruta.startswith("/"):
        try:
            ftp.cwd("/")
        except error_perm:
            pass

    for parte in partes:
        try:
            ftp.cwd(parte)
        except error_perm:
            ftp.mkd(parte)
            ftp.cwd(parte)


def subir_directorio(ftp, carpeta):
    for elemento in sorted(carpeta.iterdir()):
        if elemento.name in EXCLUIR or elemento.suffix == ".pyc":
            continue

        if elemento.is_dir():
            try:
                ftp.mkd(elemento.name)
            except error_perm:
                pass
            ftp.cwd(elemento.name)
            subir_directorio(ftp, elemento)
            ftp.cwd("..")
        else:
            with elemento.open("rb") as archivo:
                ftp.storbinary(f"STOR {elemento.name}", archivo)
            print(f"Subido: {elemento.relative_to(BASE_DIR)}")


def main():
    host = os.getenv("FTP_HOST", "").strip()
    port = int(os.getenv("FTP_PORT", "21"))
    usuario = os.getenv("FTP_USER", "").strip()
    clave = os.getenv("FTP_PASSWORD", "")
    remoto = os.getenv("FTP_REMOTE_DIR", "/materials_fadrell").strip()
    usar_tls = os.getenv("FTP_USE_TLS", "False").lower() == "true"

    if not host or not usuario or not clave:
        raise SystemExit(
            "Faltan FTP_HOST, FTP_USER o FTP_PASSWORD en el archivo .env."
        )

    clase = FTP_TLS_SesionReutilizable if usar_tls else FTP
    ftp = clase()
    ftp.connect(host, port, timeout=30)
    ftp.login(usuario, clave)

    if usar_tls:
        ftp.prot_p()

    ftp.set_pasv(True)
    asegurar_directorio(ftp, remoto)
    subir_directorio(ftp, BASE_DIR)
    ftp.quit()

    print("Proyecto subido correctamente al FTP.")


if __name__ == "__main__":
    main()
