import os
from dotenv import load_dotenv

load_dotenv()


def configurar_app(app):
    app.secret_key = os.getenv("SECRET_KEY", "chave-padrao-local")

    mysql_user = os.getenv("MYSQLUSER")
    mysql_password = os.getenv("MYSQLPASSWORD")
    mysql_host = os.getenv("MYSQLHOST")
    mysql_port = os.getenv("MYSQLPORT")
    mysql_database = os.getenv("MYSQLDATABASE")

    if not all([mysql_user, mysql_password, mysql_host, mysql_port, mysql_database]):
        raise RuntimeError(
            "Erro: variáveis do MySQL não configuradas. "
            "Configure MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLPORT e MYSQLDATABASE no .env."
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False