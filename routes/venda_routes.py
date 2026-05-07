from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.modelos import Cliente, Produto, Venda, ItemVenda, Pagamento


venda_bp = Blueprint("venda", __name__)


def logado():
    return "usuario_id" in session


@venda_bp.route("/vendas", methods=["GET", "POST"])
def vendas():
    if not logado():
        return redirect(url_for("auth.login"))

    clientes = Cliente.query.order_by(Cliente.nome).all()
    produtos = Produto.query.order_by(Produto.nome).all()

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        data_compra = request.form["data_compra"]
        prazo = request.form["prazo_pagamento"]

        produtos_ids = request.form.getlist("produto_id[]")
        quantidades = request.form.getlist("quantidade[]")

        venda = Venda(
            cliente_id=cliente_id,
            data_compra=data_compra,
            prazo_pagamento=prazo,
            total=0,
            valor_pago=0,
            valor_restante=0,
            status="Pendente"
        )

        db.session.add(venda)
        db.session.flush()

        total = 0

        for produto_id, quantidade in zip(produtos_ids, quantidades):
            if not produto_id or not quantidade:
                continue

            produto = Produto.query.get(int(produto_id))
            quantidade = float(quantidade)

            if quantidade <= 0:
                continue

            if produto.estoque < quantidade:
                flash(f"Estoque insuficiente para {produto.nome}.")
                db.session.rollback()
                return redirect(url_for("venda.vendas"))

            subtotal = produto.preco * quantidade
            total += subtotal

            item = ItemVenda(
                venda_id=venda.id,
                produto_id=produto.id,
                produto_nome=produto.nome,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                subtotal=subtotal
            )

            produto.estoque -= quantidade
            db.session.add(item)

        venda.total = total
        venda.valor_restante = total

        db.session.commit()

        flash("Venda registrada com sucesso.")
        return redirect(url_for("venda.vendas"))

    lista_vendas = Venda.query.order_by(Venda.id.desc()).all()

    return render_template(
        "vendas.html",
        clientes=clientes,
        produtos=produtos,
        vendas=lista_vendas
    )


@venda_bp.route("/pagamentos/<int:venda_id>", methods=["GET", "POST"])
def pagamentos(venda_id):
    if not logado():
        return redirect(url_for("auth.login"))

    venda = Venda.query.get_or_404(venda_id)

    if request.method == "POST":
        valor = float(request.form["valor"])

        if valor <= 0:
            flash("Informe um valor válido.")
            return redirect(url_for("venda.pagamentos", venda_id=venda.id))

        pagamento = Pagamento(venda_id=venda.id, valor=valor)

        venda.valor_pago += valor
        venda.valor_restante = venda.total - venda.valor_pago

        if venda.valor_restante <= 0:
            venda.valor_restante = 0
            venda.status = "Quitado"
        elif venda.valor_pago > 0:
            venda.status = "Parcial"
        else:
            venda.status = "Pendente"

        db.session.add(pagamento)
        db.session.commit()

        flash("Pagamento registrado.")
        return redirect(url_for("venda.pagamentos", venda_id=venda.id))

    return render_template("pagamentos.html", venda=venda)


@venda_bp.route("/vendas/excluir/<int:venda_id>")
def excluir_venda(venda_id):
    if not logado():
        return redirect(url_for("auth.login"))

    venda = Venda.query.get_or_404(venda_id)

    if venda.status != "Quitado":
        flash("Só é possível excluir vendas quitadas.")
        return redirect(url_for("venda.vendas"))

    db.session.delete(venda)
    db.session.commit()

    flash("Venda quitada excluída com sucesso.")
    return redirect(url_for("venda.vendas"))