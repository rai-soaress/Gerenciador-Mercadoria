from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.cliente_routes import cliente_bp
from routes.produto_routes import produto_bp
from routes.venda_routes import venda_bp
from routes.pdf_routes import pdf_bp
from routes.relatorio_routes import relatorio_bp


def registrar_rotas(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(venda_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(relatorio_bp)