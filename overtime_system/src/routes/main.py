from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import ClientePotencial, ClienteFinalizado
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.nome)

@main.route('/clientes_potenciais')
@login_required
def clientes_potenciais():
    clientes = ClientePotencial.query.all()
    return render_template('clientes_potenciais.html', clientes=clientes)

@main.route('/clientes_finalizados')
@login_required
def clientes_finalizados():
    clientes = ClienteFinalizado.query.all()
    return render_template('clientes_finalizados.html', clientes=clientes)

@main.route('/novo_cliente_potencial', methods=['GET', 'POST'])
@login_required
def novo_cliente_potencial():
    form = ClientePotencialForm()
    if form.validate_on_submit():
        novo_cliente = ClientePotencial(
            nome_cliente=form.nome_cliente.data,
            cpf_cnpj=form.cpf_cnpj.data,
            telefone=form.telefone.data,
            email=form.email.data,
            origem=form.origem.data,
            status=form.status.data,
            observacoes=form.observacoes.data,
            responsavel_id=current_user.id
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente potencial adicionado com sucesso!', 'success')
        return redirect(url_for('main.clientes_potenciais'))
    return render_template('novo_cliente_potencial.html', form=form)

@main.route('/novo_cliente_finalizado', methods=['GET', 'POST'])
@login_required
def novo_cliente_finalizado():
    form = ClienteFinalizadoForm()
    if form.validate_on_submit():
        # Lógica para salvar o arquivo e obter o caminho
        # Exemplo: file_path = save_file(form.documento.data)
        # Certifique-se de que a função save_file está definida e funciona corretamente
        
        # Supondo que 'save_file' retorna o caminho do arquivo ou None se não houver arquivo
        doc_rg_cnh_path = None
        if form.documento_rg_cnh.data:
            doc_rg_cnh_path = save_file(form.documento_rg_cnh.data, form.cpf.data, "rg_cnh")

        comprovante_endereco_path = None
        if form.comprovante_endereco.data:
            comprovante_endereco_path = save_file(form.comprovante_endereco.data, form.cpf.data, "comprovante_endereco")

        comprovante_pagamento_path = None
        if form.comprovante_pagamento.data:
            comprovante_pagamento_path = save_file(form.comprovante_pagamento.data, form.cpf.data, "comprovante_pagamento")

        documento_adicional_path = None
        if form.documento_adicional.data:
            documento_adicional_path = save_file(form.documento_adicional.data, form.cpf.data, "documento_adicional")

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
            honorarios_contratuais=form.honorarios_contratuais.data,
            liquido_comprado=form.liquido_comprado.data,
            resultado_esperado=form.resultado_esperado.data,
            percentual_ganho=form.percentual_ganho.data,
            valor_depositado_judicial=form.valor_depositado_judicial.data,
            liquido_a_levantar=form.liquido_a_levantar.data,
            numero_conta_judicial=form.numero_conta_judicial.data,
            data_alvara=form.data_alvara.data,
            valor_recebido_empresa=form.valor_recebido_empresa.data,
            data_recebimento_empresa=form.data_recebimento_empresa.data,
            resultado_final=form.resultado_final.data,
            tributacao=form.tributacao.data,
            observacao=form.observacao.data,
            responsavel_id=current_user.id,
            documento_rg_cnh_path=doc_rg_cnh_path,
            comprovante_endereco_path=comprovante_endereco_path,
            comprovante_pagamento_path=comprovante_pagamento_path,
            documento_adicional_path=documento_adicional_path
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cliente finalizado cadastrado com sucesso!', 'success')
        return redirect(url_for('main.clientes_finalizados'))
    return render_template('clientes_finalizados.html', title='Clientes Finalizados', form=form)


@main.route("/clientes_potenciais/delete/<int:cliente_id>", methods=['POST'])
@login_required
def delete_cliente_potencial(cliente_id):
    cliente = ClientePotencial.query.get_or_404(cliente_id)
    if cliente.responsavel_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente potencial excluído com sucesso!', 'success')
    return redirect(url_for('main.clientes_potenciais'))

@main.route("/clientes_finalizados/delete/<int:cliente_id>", methods=['POST'])
@login_required
def delete_cliente_finalizado(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    if cliente.responsavel_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente finalizado excluído com sucesso!', 'success')
    return redirect(url_for('main.clientes_finalizados'))

@main.route("/clientes_potenciais/edit/<int:cliente_id>", methods=['GET', 'POST'])
@login_required
def edit_cliente_potencial(cliente_id):
    cliente = ClientePotencial.query.get_or_404(cliente_id)
    if cliente.responsavel_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = ClientePotencialForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nome_cliente = form.nome_cliente.data
        cliente.cpf = form.cpf.data
        cliente.telefone = form.telefone.data
        cliente.email = form.email.data
        cliente.data_nascimento = form.data_nascimento.data
        cliente.rg = form.rg.data
        cliente.endereco_completo = form.endereco_completo.data
        cliente.processo_judicial_numero = form.processo_judicial_numero.data
        cliente.vara_comarca = form.vara_comarca.data
        cliente.valor_inscrito_requisitado = form.valor_inscrito_requisitado.data
        cliente.banco = form.banco.data
        cliente.agencia = form.agencia.data
        cliente.conta_corrente = form.conta_corrente.data
        cliente.status_interesse = form.status_interesse.data
        cliente.observacoes = form.observacoes.data
        cliente.data_primeiro_contato = form.data_primeiro_contato.data
        db.session.commit()
        flash('Cliente potencial atualizado com sucesso!', 'success')
        return redirect(url_for('main.clientes_potenciais'))
    return render_template('edit_cliente_potencial.html', title='Editar Cliente Potencial', form=form, cliente=cliente)

@main.route("/clientes_finalizados/edit/<int:cliente_id>", methods=['GET', 'POST'])
@login_required
def edit_cliente_finalizado(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    if cliente.responsavel_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = ClienteFinalizadoForm(obj=cliente)
    if form.validate_on_submit():
        cliente.cliente_nome = form.cliente_nome.data
        cliente.cpf = form.cpf.data
        cliente.numero_processo = form.numero_processo.data
        cliente.vara = form.vara.data
        cliente.precatorio = form.precatorio.data
        cliente.n_cnj = form.n_cnj.data
        cliente.of_requisitorio = form.of_requisitorio.data
        cliente.percentual_cessao = form.percentual_cessao.data
        cliente.ano_previsto_pagamento = form.ano_previsto_pagamento.data
        cliente.preco_aquisicao = form.preco_aquisicao.data
        cliente.data_calculo = form.data_calculo.data
        cliente.data_compra = form.data_compra.data
        cliente.local_compra = form.local_compra.data
        cliente.data_pagamento_cliente = form.data_pagamento_cliente.data
        cliente.valor_inscrito_requisitado = form.valor_inscrito_requisitado.data
        cliente.honorarios_contratuais = form.honorarios_contratuais.data
        cliente.liquido_comprado = form.liquido_comprado.data
        cliente.resultado_esperado = form.resultado_esperado.data
        cliente.percentual_ganho = form.percentual_ganho.data
        cliente.valor_depositado_judicial = form.valor_depositado_judicial.data
        cliente.liquido_a_levantar = form.liquido_a_levantar.data
        cliente.numero_conta_judicial = form.numero_conta_judicial.data
        cliente.data_alvara = form.data_alvara.data
        cliente.valor_recebido_empresa = form.valor_recebido_empresa.data
        cliente.data_recebimento_empresa = form.data_recebimento_empresa.data
        cliente.resultado_final = form.resultado_final.data
        cliente.tributacao = form.tributacao.data
        cliente.banco_cliente = form.banco_cliente.data
        cliente.observacao = form.observacao.data
        db.session.commit()
        flash('Cliente finalizado atualizado com sucesso!', 'success')
        return redirect(url_for('main.clientes_finalizados'))
    return render_template('edit_cliente_finalizado.html', title='Editar Cliente Finalizado', form=form, cliente=cliente)

