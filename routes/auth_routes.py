import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.modelos import Sistema, Usuario, Cliente, Produto, Venda, ItemVenda, Pagamento


auth_bp = Blueprint("auth", __name__)


def logado():
    return "usuario_id" in session


def verificar_ativacao():
    sistema = Sistema.query.first()
    return sistema and sistema.ativado


@auth_bp.route("/")
def inicio():
    if not verificar_ativacao():
        return redirect(url_for("auth.ativacao"))

    if Usuario.query.count() == 0:
        return redirect(url_for("auth.criar_admin"))

    return redirect(url_for("auth.login"))


@auth_bp.route("/ativacao", methods=["GET", "POST"])
def ativacao():
    if verificar_ativacao():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        senha_digitada = request.form["senha"]

        if senha_digitada == os.getenv("SENHA_MESTRE"):
            sistema = Sistema.query.first()
            sistema.ativado = True
            db.session.commit()

            flash("Sistema ativado com sucesso.")
            return redirect(url_for("auth.criar_admin"))

        flash("Senha mestre incorreta.")

    return render_template("ativacao.html")


@auth_bp.route("/criar-admin", methods=["GET", "POST"])
def criar_admin():
    if not verificar_ativacao():
        return redirect(url_for("auth.ativacao"))

    if Usuario.query.count() > 0:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        novo_usuario = Usuario(
            nome=request.form["nome"],
            email=request.form["email"],
            senha=generate_password_hash(request.form["senha"])
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Administrador criado com sucesso.")
        return redirect(url_for("auth.login"))

    return render_template("criar_admin.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if not verificar_ativacao():
        return redirect(url_for("auth.ativacao"))

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("dashboard.dashboard"))

        flash("E-mail ou senha incorretos.")

    return render_template("login.html")


@auth_bp.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form["email"]
        senha_mestre = request.form["senha_mestre"]
        nova_senha = request.form["nova_senha"]

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash("Usuário não encontrado.")
            return redirect(url_for("auth.recuperar_senha"))

        if senha_mestre != os.getenv("SENHA_MESTRE"):
            flash("Senha mestre incorreta.")
            return redirect(url_for("auth.recuperar_senha"))

        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()

        flash("Senha alterada com sucesso.")
        return redirect(url_for("auth.login"))

    return render_template("recuperar_senha.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/confirmar-exclusao", methods=["GET", "POST"])
def confirmar_exclusao():
    if not logado():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        senha_mestre = request.form["senha_mestre"]

        if senha_mestre != os.getenv("SENHA_MESTRE"):
            flash("Senha mestre incorreta. Exclusão cancelada.")
            return redirect(url_for("auth.confirmar_exclusao"))

        Pagamento.query.delete()
        ItemVenda.query.delete()
        Venda.query.delete()
        Produto.query.delete()
        Cliente.query.delete()
        Usuario.query.delete()

        sistema = Sistema.query.first()
        if sistema:
            sistema.ativado = False

        db.session.commit()
        session.clear()

        flash("Conta administrativa e todos os dados foram excluídos.")
        return redirect(url_for("auth.ativacao"))

    return render_template("confirmar_exclusao.html")