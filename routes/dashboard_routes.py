from flask import Blueprint, render_template, redirect, url_for, session
from models import db
from models.modelos import Cliente, Produto, Venda


dashboard_bp = Blueprint("dashboard", __name__)


def logado():
    return "usuario_id" in session


@dashboard_bp.route("/dashboard")
def dashboard():
    if not logado():
        return redirect(url_for("auth.login"))

    total_vendido = db.session.query(db.func.sum(Venda.total)).scalar() or 0
    total_recebido = db.session.query(db.func.sum(Venda.valor_pago)).scalar() or 0
    total_pendente = db.session.query(db.func.sum(Venda.valor_restante)).scalar() or 0

    clientes = Cliente.query.count()
    produtos = Produto.query.count()
    inadimplentes = Venda.query.filter(Venda.valor_restante > 0).count()
    vendas_recentes = Venda.query.order_by(Venda.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_vendido=total_vendido,
        total_recebido=total_recebido,
        total_pendente=total_pendente,
        clientes=clientes,
        produtos=produtos,
        inadimplentes=inadimplentes,
        vendas_recentes=vendas_recentes
    )