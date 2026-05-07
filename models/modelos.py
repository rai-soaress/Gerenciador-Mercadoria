from datetime import datetime
from models import db


class Sistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ativado = db.Column(db.Boolean, default=False)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class Comercio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    telefone = db.Column(db.String(30))
    endereco = db.Column(db.Text)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30))
    endereco = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    vendas = db.relationship("Venda", backref="cliente", lazy=True, cascade="all, delete")


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(80))
    preco = db.Column(db.Float, nullable=False)
    tipo_venda = db.Column(db.String(30))
    estoque = db.Column(db.Float, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)

    data_compra = db.Column(db.String(20))
    prazo_pagamento = db.Column(db.String(20))

    total = db.Column(db.Float, default=0)
    valor_pago = db.Column(db.Float, default=0)
    valor_restante = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="Pendente")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemVenda", backref="venda", lazy=True, cascade="all, delete")
    pagamentos = db.relationship("Pagamento", backref="venda", lazy=True, cascade="all, delete")


class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)

    produto_nome = db.Column(db.String(120))
    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)


class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)

    valor = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)