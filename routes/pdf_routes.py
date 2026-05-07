from flask import Blueprint, send_file, redirect, url_for, session
from fpdf import FPDF
from models.modelos import Cliente, Venda


pdf_bp = Blueprint("pdf", __name__)


def logado():
    return "usuario_id" in session


@pdf_bp.route("/pdf-cliente/<int:cliente_id>")
def pdf_cliente(cliente_id):
    if not logado():
        return redirect(url_for("auth.login"))

    cliente = Cliente.query.get_or_404(cliente_id)

    vendas = Venda.query.filter_by(
        cliente_id=cliente.id
    ).order_by(Venda.id.desc()).all()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Extrato do Cliente", ln=True, align="C")

    pdf.ln(8)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Cliente: {cliente.nome}", ln=True)
    pdf.cell(0, 8, f"Telefone: {cliente.telefone}", ln=True)
    pdf.cell(0, 8, f"Endereco: {cliente.endereco}", ln=True)

    pdf.ln(5)

    total_geral = 0
    total_pago = 0
    total_restante = 0

    for venda in vendas:
        total_geral += venda.total
        total_pago += venda.valor_pago
        total_restante += venda.valor_restante

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Venda #{venda.id}", ln=True)

        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"Total: R$ {venda.total:.2f}", ln=True)
        pdf.cell(0, 8, f"Pago: R$ {venda.valor_pago:.2f}", ln=True)
        pdf.cell(0, 8, f"Restante: R$ {venda.valor_restante:.2f}", ln=True)
        pdf.cell(0, 8, f"Status: {venda.status}", ln=True)

        pdf.cell(0, 8, "Produtos:", ln=True)

        for item in venda.itens:
            pdf.cell(
                0,
                8,
                f"- {item.produto_nome} | Qtd: {item.quantidade} | R$ {item.subtotal:.2f}",
                ln=True
            )

        pdf.cell(0, 8, "Pagamentos:", ln=True)

        for pagamento in venda.pagamentos:
            pdf.cell(
                0,
                8,
                f"- R$ {pagamento.valor:.2f} em {pagamento.criado_em.strftime('%d/%m/%Y')}",
                ln=True
            )

        pdf.ln(4)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Total geral: R$ {total_geral:.2f}", ln=True)
    pdf.cell(0, 8, f"Total pago: R$ {total_pago:.2f}", ln=True)
    pdf.cell(0, 8, f"Total restante: R$ {total_restante:.2f}", ln=True)

    nome_arquivo = f"cliente_{cliente.id}.pdf"
    pdf.output(nome_arquivo)

    return send_file(nome_arquivo, as_attachment=True)