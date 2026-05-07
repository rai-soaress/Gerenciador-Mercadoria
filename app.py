from flask import Flask
from config import configurar_app
from models import db
from models.modelos import Sistema
from routes import registrar_rotas


app = Flask(__name__)

configurar_app(app)

db.init_app(app)

registrar_rotas(app)


with app.app_context():
    db.create_all()

    if not Sistema.query.first():
        sistema = Sistema(ativado=False)
        db.session.add(sistema)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)