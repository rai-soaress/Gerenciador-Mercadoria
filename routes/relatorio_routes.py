from flask import Blueprint, render_template, request, redirect, url_for, session
from models.modelos import Venda


relatorio_bp = Blueprint("relatorio", __name__)


def logado():
    return "usuario_id" in session


@relatorio_bp.route("/relatorios")
def relatorios():
    if not logado():
        return redirect(url_for("auth.login"))

    mes = request.args.get("mes", "")
    ano = request.args.get("ano", "")

    vendas = []

    if mes and ano:
        prefixo = f"{ano}-{mes.zfill(2)}"
        vendas = Venda.query.filter(
            Venda.data_compra.like(f"{prefixo}%")
        ).order_by(Venda.id.desc()).all()

    total_vendido = sum(venda.total for venda in vendas)
    total_recebido = sum(venda.valor_pago for venda in vendas)
    total_pendente = sum(venda.valor_restante for venda in vendas)

    return render_template(
        "relatorios.html",
        vendas=vendas,
        mes=mes,
        ano=ano,
        total_vendido=total_vendido,
        total_recebido=total_recebido,
        total_pendente=total_pendente
    )