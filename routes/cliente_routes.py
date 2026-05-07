from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.modelos import Cliente, Venda


cliente_bp = Blueprint("cliente", __name__)


def logado():
    return "usuario_id" in session


@cliente_bp.route("/clientes", methods=["GET", "POST"])
def clientes():

    if not logado():
        return redirect(url_for("auth.login"))

    busca = request.args.get("busca", "").strip()

    # CADASTRAR CLIENTE
    if request.method == "POST":

        cliente = Cliente(
            nome=request.form["nome"],
            telefone=request.form["telefone"],
            endereco=request.form["endereco"],
            observacoes=request.form["observacoes"]
        )

        db.session.add(cliente)
        db.session.commit()

        flash("Cliente cadastrado com sucesso.")

        return redirect(url_for("cliente.clientes"))

    # BUSCA DE CLIENTE
    if busca:

        lista = Cliente.query.filter(
            Cliente.nome.ilike(f"%{busca}%")
        ).order_by(Cliente.nome).all()

    else:

        lista = Cliente.query.order_by(Cliente.nome).all()

    return render_template(
        "clientes.html",
        clientes=lista,
        busca=busca
    )


@cliente_bp.route("/clientes/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar_cliente(cliente_id):

    if not logado():
        return redirect(url_for("auth.login"))

    cliente = Cliente.query.get_or_404(cliente_id)

    if request.method == "POST":

        cliente.nome = request.form["nome"]
        cliente.telefone = request.form["telefone"]
        cliente.endereco = request.form["endereco"]
        cliente.observacoes = request.form["observacoes"]

        db.session.commit()

        flash("Cliente atualizado com sucesso.")

        return redirect(url_for("cliente.clientes"))

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


@cliente_bp.route("/clientes/excluir/<int:cliente_id>")
def excluir_cliente(cliente_id):

    if not logado():
        return redirect(url_for("auth.login"))

    cliente = Cliente.query.get_or_404(cliente_id)

    vendas_abertas = Venda.query.filter(
        Venda.cliente_id == cliente.id,
        Venda.status != "Quitado"
    ).first()

    if vendas_abertas:

        flash(
            "Não é possível excluir este cliente porque ele possui dívidas pendentes."
        )

        return redirect(url_for("cliente.clientes"))

    db.session.delete(cliente)
    db.session.commit()

    flash("Cliente excluído com sucesso.")

    return redirect(url_for("cliente.clientes"))


@cliente_bp.route("/historico-cliente/<int:cliente_id>")
def historico_cliente(cliente_id):

    if not logado():
        return redirect(url_for("auth.login"))

    cliente = Cliente.query.get_or_404(cliente_id)

    vendas = Venda.query.filter_by(
        cliente_id=cliente.id
    ).order_by(Venda.id.desc()).all()

    return render_template(
        "historico_cliente.html",
        cliente=cliente,
        vendas=vendas
    )