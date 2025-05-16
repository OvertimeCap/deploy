from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from src.models import ClientePotencial, ClienteFinalizado, User # Alterado para importação absoluta
from src import db # Alterado para importação absoluta
from src.forms import ClientePotencialForm, ClienteFinalizadoForm, LoginForm # Alterado para importação absoluta
import os
from werkzeug.utils import secure_filename
from src.contract_generator import generate_contract_docx # Alterado para importação absoluta
from io import BytesIO

main_bp = Blueprint("main", __name__)


def save_file(file_data, cpf_cliente, subfolder_prefix):
    if not file_data:
        return None
    filename = secure_filename(file_data.filename)
    # Criar um nome de subpasta mais específico para o cliente e tipo de doc
    # Removendo caracteres inválidos do CPF para nome de pasta
    safe_cpf = "".join(filter(str.isalnum, cpf_cliente))
    upload_subfolder = os.path.join(safe_cpf, subfolder_prefix)
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], upload_subfolder)
    
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    file_data.save(file_path)
    # Retornar o caminho relativo a partir da pasta UPLOAD_FOLDER para armazenamento no BD
    return os.path.join(upload_subfolder, filename)

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
        doc_rg_cnh_path = save_file(form.documento_rg_cnh.data, form.cpf.data, "rg_cnh") if form.documento_rg_cnh.data else None
        comprovante_endereco_path = save_file(form.comprovante_endereco.data, form.cpf.data, "comprovante_endereco") if form.comprovante_endereco.data else None
        comprovante_pagamento_path = save_file(form.comprovante_pagamento.data, form.cpf.data, "comprovante_pagamento") if form.comprovante_pagamento.data else None
        documento_adicional_path = save_file(form.documento_adicional.data, form.cpf.data, "documento_adicional") if form.documento_adicional.data else None

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
            banco_cliente=form.banco_cliente.data,
            observacao=form.observacao.data,
            status_tarefa=form.status_tarefa.data,
            responsavel_id=current_user.id,
            documento_rg_cnh_path=doc_rg_cnh_path,
            comprovante_endereco_path=comprovante_endereco_path,
            comprovante_pagamento_path=comprovante_pagamento_path,
            documento_adicional_path=documento_adicional_path
        )
        db.session.add(novo_cliente)
        db.session.commit()
        flash("Cliente finalizado cadastrado com sucesso!", "success")
        return redirect(url_for("main.clientes_finalizados"))
    clientes = ClienteFinalizado.query.order_by(ClienteFinalizado.data_compra.desc()).all()
    return render_template("clientes_finalizados.html", title="Clientes Finalizados", form=form, clientes=clientes)

@main_bp.route("/painel_tarefas", methods=["GET", "POST"])
@login_required
def painel_tarefas():
    status_filter = request.args.get("status_tarefa", "todos")
    query = ClienteFinalizado.query
    if not current_user.is_admin:
        query = query.filter_by(responsavel_id=current_user.id)

    if status_filter != "todos" and status_filter:
        query = query.filter_by(status_tarefa=status_filter)
    
    clientes = query.order_by(ClienteFinalizado.data_compra.desc()).all()
    return render_template("painel_tarefas.html", title="Painel de Tarefas", clientes=clientes, current_filter=status_filter)

@main_bp.route("/painel_tarefas/update_observacao/<int:cliente_id>", methods=["POST"])
@login_required
def update_observacao_tarefa(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    if not current_user.is_admin and cliente.responsavel_id != current_user.id:
        flash("Você não tem permissão para editar esta tarefa.", "danger")
        return redirect(url_for("main.painel_tarefas"))
    nova_observacao = request.form.get("observacao")
    cliente.observacao = nova_observacao
    db.session.commit()
    flash("Observação atualizada com sucesso!", "success")
    return redirect(url_for("main.painel_tarefas"))

@main_bp.route("/painel_tarefas/update_status/<int:cliente_id>", methods=["POST"])
@login_required
def update_status_tarefa(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    if not current_user.is_admin and cliente.responsavel_id != current_user.id:
        flash("Você não tem permissão para editar esta tarefa.", "danger")
        return redirect(url_for("main.painel_tarefas"))
    novo_status = request.form.get("status_tarefa")
    cliente.status_tarefa = novo_status
    db.session.commit()
    flash("Status da tarefa atualizado com sucesso!", "success")
    return redirect(url_for("main.painel_tarefas"))

@main_bp.route("/gerar_contrato/<int:cliente_id>")
@login_required
def gerar_contrato(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    # Adicione mais campos conforme necessário para o contrato
    context = {
        "CLIENTE": cliente.cliente_nome,
        "CPF": cliente.cpf,
        "PROCESSO": cliente.numero_processo,
        "VARA": cliente.vara,
        # ... outros campos do cliente que estão no contrato
    }
    # Caminho para o template do contrato
    template_path = os.path.join(current_app.root_path, "..", "Contrato_OVERTIME_Modelo.docx") 
    
    if not os.path.exists(template_path):
        flash(f"Modelo de contrato não encontrado em {template_path}", "danger")
        return redirect(url_for("main.clientes_finalizados"))

    try:
        contrato_bytes = generate_contract_docx(template_path, context)
        return send_from_directory(
            directory=os.path.dirname(contrato_bytes), # Gunicorn precisa de um dir
            path=os.path.basename(contrato_bytes),
            as_attachment=True,
            download_name=f"Contrato_{cliente.cliente_nome.replace(" ", "_")}_{cliente.cpf}.docx"
        )
    except Exception as e:
        flash(f"Erro ao gerar contrato: {e}", "danger")
        current_app.logger.error(f"Erro ao gerar contrato para cliente {cliente_id}: {e}")
        return redirect(url_for("main.clientes_finalizados"))

@main_bp.route("/uploads/<path:filepath>")
@login_required
def uploaded_file(filepath):
    # filepath aqui será algo como "cpf_cliente/subfolder_prefix/filename.ext"
    # Precisamos garantir que o usuário só acesse seus próprios arquivos ou seja admin
    # Esta é uma implementação básica, pode precisar de mais lógica de permissão
    # dependendo de como os arquivos são associados aos usuários/clientes.
    
    # Extrair CPF da pasta para verificação de permissão (exemplo)
    # Isso assume que o CPF está no início do filepath
    # cpf_from_path = filepath.split(os.sep)[0]
    # cliente_associado = ClienteFinalizado.query.filter_by(cpf=cpf_from_path).first()
    # if not current_user.is_admin and (not cliente_associado or cliente_associado.responsavel_id != current_user.id):
    #     abort(403) # Proibido
        
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filepath)

# Rotas de edição e exclusão (simplificadas, adicione lógica de permissão se necessário)
@main_bp.route("/clientes_potenciais/edit/<int:cliente_id>", methods=["GET", "POST"])
@login_required
def edit_cliente_potencial(cliente_id):
    cliente = ClientePotencial.query.get_or_404(cliente_id)
    if not current_user.is_admin and cliente.responsavel_id != current_user.id:
        abort(403)
    form = ClientePotencialForm(obj=cliente)
    if form.validate_on_submit():
        form.populate_obj(cliente)
        db.session.commit()
        flash("Cliente potencial atualizado com sucesso!", "success")
        return redirect(url_for("main.clientes_potenciais"))
    return render_template("edit_cliente_potencial.html", title="Editar Cliente Potencial", form=form, cliente=cliente)

@main_bp.route("/clientes_potenciais/delete/<int:cliente_id>", methods=["POST"])
@login_required
def delete_cliente_potencial(cliente_id):
    cliente = ClientePotencial.query.get_or_404(cliente_id)
    if not current_user.is_admin and cliente.responsavel_id != current_user.id:
        abort(403)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente potencial excluído com sucesso!", "success")
    return redirect(url_for("main.clientes_potenciais"))

@main_bp.route("/clientes_finalizados/edit/<int:cliente_id>", methods=["GET", "POST"])
@login_required
def edit_cliente_finalizado(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    if not current_user.is_admin and cliente.responsavel_id != current_user.id:
        abort(403)
    form = ClienteFinalizadoForm(obj=cliente)
    if form.validate_on_submit():
        # Manter os caminhos dos arquivos existentes se nenhum novo arquivo for enviado
        if not form.documento_rg_cnh.data:
            form.documento_rg_cnh.data = cliente.documento_rg_cnh_path
        else:
            cliente.documento_rg_cnh_path = save_file(form.documento_rg_cnh.data, cliente.cpf, "rg_cnh")
        
        if not form.comprovante_endereco.data:
            form.comprovante_endereco.data = cliente.comprovante_endereco_path
        else:
            cliente.comprovante_endereco_path = save_file(form.comprovante_endereco.data, cliente.cpf, "comprovante_endereco")

        if not form.comprovante_pagamento.data:
            form.comprovante_pagamento.data = cliente.comprovante_pagamento_path
        else:
            cliente.comprovante_pagamento_path = save_file(form.comprovante_pagamento.data, cliente.cpf, "comprovante_pagamento")

        if not form.documento_adicional.data:
            form.documento_adicional.data = cliente.documento_adicional_path
        else:
            cliente.documento_adicional_path = save_file(form.documento_adicional.data, cliente.cpf, "documento_adicional")
        
        # Popula o objeto cliente com os dados do formulário, exceto os campos de arquivo que já tratamos
        form_fields_to_populate = {key: value for key, value in form.data.items() if not key.startswith("documento") and not key.startswith("comprovante")}
        for key, value in form_fields_to_populate.items():
            setattr(cliente, key, value)
            
        db.session.commit()
        flash("Cliente finalizado atualizado com sucesso!", "success")
        return redirect(url_for("main.clientes_finalizados"))
    
    # Para exibir os nomes dos arquivos atuais no formulário de edição
    # (isso é mais para a lógica do template, mas pode ser preparado aqui)
    # form.documento_rg_cnh.label.text = f"RG/CNH (Atual: {cliente.documento_rg_cnh_path or \"Nenhum\"})"
    # ... e assim por diante para outros arquivos

    return render_template("edit_cliente_finalizado.html", title="Editar Cliente Finalizado", form=form, cliente=cliente)

@main_bp.route("/clientes_finalizados/delete/<int:cliente_id>", methods=["POST"])
@login_required
def delete_cliente_finalizado(cliente_id):
    cliente = ClienteFinalizado.query.get_or_404(cliente_id)
    if not current_user.is_admin and cliente.responsavel_id != current_user.id:
        abort(403)
    # Opcional: deletar arquivos do sistema de arquivos
    # if cliente.documento_rg_cnh_path: os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], cliente.documento_rg_cnh_path))
    # ... e para outros arquivos
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente finalizado excluído com sucesso!", "success")
    return redirect(url_for("main.clientes_finalizados"))

