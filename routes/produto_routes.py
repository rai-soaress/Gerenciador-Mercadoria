from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.modelos import Produto, ItemVenda


produto_bp = Blueprint("produto", __name__)


def logado():
    return "usuario_id" in session


@produto_bp.route("/produtos", methods=["GET", "POST"])
def produtos():
    if not logado():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        produto = Produto(
            nome=request.form["nome"],
            categoria=request.form["categoria"],
            preco=float(request.form["preco"]),
            tipo_venda=request.form["tipo_venda"],
            estoque=float(request.form["estoque"])
        )

        db.session.add(produto)
        db.session.commit()

        flash("Produto cadastrado com sucesso.")
        return redirect(url_for("produto.produtos"))

    lista = Produto.query.order_by(Produto.nome).all()

    return render_template("produtos.html", produtos=lista)


@produto_bp.route("/produtos/editar/<int:produto_id>", methods=["GET", "POST"])
def editar_produto(produto_id):
    if not logado():
        return redirect(url_for("auth.login"))

    produto = Produto.query.get_or_404(produto_id)

    if request.method == "POST":
        produto.nome = request.form["nome"]
        produto.categoria = request.form["categoria"]
        produto.preco = float(request.form["preco"])
        produto.tipo_venda = request.form["tipo_venda"]
        produto.estoque = float(request.form["estoque"])

        db.session.commit()

        flash("Produto atualizado com sucesso.")
        return redirect(url_for("produto.produtos"))

    return render_template("editar_produto.html", produto=produto)


@produto_bp.route("/produtos/excluir/<int:produto_id>")
def excluir_produto(produto_id):
    if not logado():
        return redirect(url_for("auth.login"))

    produto = Produto.query.get_or_404(produto_id)

    produto_em_venda = ItemVenda.query.filter_by(
        produto_id=produto.id
    ).first()

    if produto_em_venda:
        flash("Não é possível excluir este produto porque ele já possui vendas registradas.")
        return redirect(url_for("produto.produtos"))

    db.session.delete(produto)
    db.session.commit()

    flash("Produto excluído com sucesso.")
    return redirect(url_for("produto.produtos"))