from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from src.models import ClientePotencial, ClienteFinalizado
from src.forms import ClientePotencialForm, ClienteFinalizadoForm
from src.contract_generator import generate_contract_docx
from src import db
import os

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    return render_template("index.html", title="Página Inicial")

@main_bp.route("/clientes_potenciais", methods=["GET", "POST"])
@login_required
def clientes_potenciais():
    form = ClientePotencialForm()
    if form.validate_on_submit():
        novo_cliente = ClientePotencial(
            nome_cliente=form.nome_cliente.data,
            cpf=form.cpf.data,
            telefone=form.telefone.data,
            email=form.email.data,
            data_nascimento=form.data_nascimento.data,
            rg=form.rg.data,
            endereco_completo=form.endereco_completo.data,
            processo_judicial_numero=form.processo_judicial_numero.data,
            vara_comarca=form.vara_comarca.data,
            valor_inscrito_requisitado=form.valor_inscrito_requisitado.data,
            banco=form.banco.data,
            agencia=form.agencia.data,
            conta_corrente=form.conta_corrente.data,
            status_interesse=form.status_interesse.data,
            observacoes=form.observacoes.data,
            data_primeiro_contato=form.data_primeiro_contato.data,
            status_tarefa=form.status_tarefa.data,
            responsavel_id=current_user.id
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash("Cliente potencial adicionado com sucesso!", "success")
        return redirect(url_for("main.clientes_potenciais"))

    status_filter = request.args.get("status_interesse", "todos")
    if status_filter == "todos" or not status_filter:
        clientes = ClientePotencial.query.order_by(ClientePotencial.data_primeiro_contato.desc()).all()
    else:
        clientes = ClientePotencial.query.filter_by(status_interesse=status_filter).order_by(ClientePotencial.data_primeiro_contato.desc()).all()

    return render_template("clientes_potenciais.html", title="Clientes Potenciais", form=form, clientes=clientes, current_filter=status_filter)

@main_bp.route("/clientes_finalizados", methods=["GET", "POST"])
@login_required
def clientes_finalizados():
    form = ClienteFinalizadoForm()
    if form.validate_on_submit():
        novo_cliente = ClienteFinalizado(
            cliente_nome=form.cliente_nome.data,
            cpf=form.cpf.data,
            numero_processo=form.numero_processo.data,
            vara=form.vara.data,
            precatorio=form.precatorio.data,
            n_cnj=form.n_cnj.data,
            of_requisitorio=form.of_requisitorio.data,
            percentual_cessao=form.percentual_cessao.data,
            ano_previsto_pagamento=form.ano_previsto_pagamento.data,
            preco_aquisicao=form.preco_aquisicao.data,
            data_calculo=form.data_calculo.data,
            data_compra=form.data_compra.data,
            local_compra=form.local_compra.data,
            data_pagamento_cliente=form.data_pagamento_cliente.data,
            valor_inscrito_requisitado=form.valor_inscrito_requisitado.data,
            observacao=form.observacao.data,
            status_tarefa=form.status_tarefa.data,
            responsavel_id=current_user.id
        )
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('main.contrato_pronto', cliente_id=novo_cliente.id))
    clientes = ClienteFinalizado.query.order_by(ClienteFinalizado.data_compra.desc()).all()
    return render_template("clientes_finalizados.html", title="Clientes Finalizados", form=form, clientes=clientes)

@main_bp.route("/clientes_finalizados/contrato_pronto/<int:cliente_id>")
@login_required
def contrato_pronto(cliente_id):
    return render_template("contrato_pronto.html", cliente_id=cliente_id)

@main_bp.route("/gerar_contrato/<int:cliente_id>")
@login_required
def gerar_contrato(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    context = {
        "CLIENTE": cliente.cliente_nome,
        "CPF": cliente.cpf,
        "PROCESSO": cliente.numero_processo,
        "VARA": cliente.vara,
    }
    template_path = os.path.join(current_app.root_path, "..", "Contrato_OVERTIME_Modelo.docx")
    if not os.path.exists(template_path):
        flash("Modelo de contrato não encontrado.", "danger")
        return redirect(url_for("main.contrato_pronto", cliente_id=cliente.id))

    try:
        contrato_path = generate_contract_docx(template_path, context)
        return send_from_directory(
            directory=os.path.dirname(contrato_path),
            path=os.path.basename(contrato_path),
            as_attachment=True,
            download_name=f"Contrato_{cliente.cliente_nome.replace(' ', '_')}_{cliente.cpf}.docx"
        )
    except Exception as e:
        flash(f"Erro ao gerar contrato: {e}", "danger")
        return redirect(url_for("main.contrato_pronto", cliente_id=cliente.id))