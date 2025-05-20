from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from src.models import ClienteFinalizado, ClientePotencial
from src.forms import ClientePotencialForm, ClienteFinalizadoForm
from src import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    return render_template("index.html", title="Página Inicial")

@main_bp.route("/clientes_finalizados/contrato_pronto/<int:cliente_id>")
@login_required
def contrato_pronto(cliente_id):
    return render_template("contrato_pronto.html", cliente_id=cliente_id)

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

@main_bp.route("/clientes_finalizados", methods=["GET"])
@login_required
def clientes_finalizados():
    form = ClienteFinalizadoForm()
    clientes = ClienteFinalizado.query.order_by(ClienteFinalizado.data_compra.desc()).all()
    return render_template("clientes_finalizados.html", title="Clientes Finalizados", form=form, clientes=clientes)