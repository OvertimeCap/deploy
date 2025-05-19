
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, Length, Regexp
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Login")

class ClientePotencialForm(FlaskForm):
    nome_cliente = StringField("Nome do Cliente", validators=[DataRequired(), Length(max=200)])
    cpf = StringField("CPF", validators=[Optional(), Regexp(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", message="Formato CPF: XXX.XXX.XXX-XX"), Length(max=14)])
    telefone = StringField("Telefone", validators=[Optional(), Length(max=20)])
    email = StringField("E-mail", validators=[Optional(), Email(), Length(max=120)])
    data_nascimento = DateField("Data de Nascimento", format="%Y-%m-%d", validators=[Optional()])
    rg = StringField("RG", validators=[Optional(), Length(max=20)])
    endereco_completo = TextAreaField("Endereço Completo", validators=[Optional(), Length(max=300)])
    processo_judicial_numero = StringField("Processo Judicial Nº", validators=[Optional(), Length(max=100)])
    vara_comarca = StringField("Vara / Comarca", validators=[Optional(), Length(max=150)])
    valor_inscrito_requisitado = FloatField("Valor Inscrito / Requisitado (R$)", validators=[DataRequired()])
    banco = StringField("Banco", validators=[Optional(), Length(max=100)])
    agencia = StringField("Agência", validators=[Optional(), Length(max=20)])
    conta_corrente = StringField("Conta Corrente", validators=[Optional(), Length(max=30)])
    status_interesse = SelectField("Status de Interesse",
                                choices=[
                                    ("em negociação", "Em Negociação"),
                                    ("sem interesse", "Sem Interesse"),
                                    ("aguardando retorno", "Aguardando Retorno")
                                ],
                                validators=[DataRequired()])
    observacoes = TextAreaField("Observações", validators=[Optional()])
    data_primeiro_contato = DateField("Data do Primeiro Contato", format="%Y-%m-%d", validators=[Optional()])
    status_tarefa = SelectField("Status da Tarefa",
                              choices=[
                                  ("pendente", "Pendente"),
                                  ("em andamento", "Em Andamento"),
                                  ("concluído", "Concluído")
                              ],
                              default="pendente",
                              validators=[DataRequired()])
    submit = SubmitField("Salvar Cliente Potencial")

class ClienteFinalizadoForm(FlaskForm):
    cliente_nome = StringField("Nome Completo do Cliente", validators=[DataRequired(), Length(max=200)])
    cpf = StringField("CPF", validators=[DataRequired(), Regexp(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", message="Formato CPF: XXX.XXX.XXX-XX"), Length(max=14)])
    numero_processo = StringField("Número do Processo", validators=[Optional(), Length(max=100)])
    vara = StringField("Vara / Comarca", validators=[Optional(), Length(max=150)])
    precatorio = StringField("Precatório", validators=[Optional(), Length(max=100)])
    n_cnj = StringField("Nº CNJ", validators=[Optional(), Length(max=100)])
    of_requisitorio = StringField("Of. Requisitório", validators=[Optional(), Length(max=100)])
    percentual_cessao = FloatField("Percentual de Cessão (%)", validators=[Optional()])
    ano_previsto_pagamento = StringField("Ano Previsto para Pagamento", validators=[Optional(), Length(max=4)])
    preco_aquisicao = FloatField("Preço de Aquisição (R$)", validators=[Optional()])
    data_calculo = DateField("Data do Cálculo", format="%Y-%m-%d", validators=[Optional()])
    data_compra = DateField("Data da Compra", format="%Y-%m-%d", validators=[Optional()])
    local_compra = StringField("Local da Compra", validators=[Optional(), Length(max=150)])
    data_pagamento_cliente = DateField("Data do Pagamento ao Cliente", format="%Y-%m-%d", validators=[Optional()])
    valor_inscrito_requisitado = FloatField("Valor Inscrito / Requisitado (R$)", validators=[Optional()])
    observacao = TextAreaField("Observação", validators=[Optional()])
    status_tarefa = SelectField("Status da Tarefa",
                              choices=[
                                  ("pendente", "Pendente"),
                                  ("em andamento", "Em Andamento"),
                                  ("concluído", "Concluído")
                              ],
                              default="pendente",
                              validators=[DataRequired()])

    documento_rg_cnh = FileField("RG ou CNH (PDF, Imagem)", validators=[Optional(), FileAllowed(["pdf", "jpg", "png", "jpeg"], "Apenas PDF e Imagens!")])
    comprovante_endereco = FileField("Comprovante de Endereço (PDF, Imagem)", validators=[Optional(), FileAllowed(["pdf", "jpg", "png", "jpeg"], "Apenas PDF e Imagens!")])
    comprovante_pagamento = FileField("Comprovante de Pagamento (PDF, Imagem)", validators=[Optional(), FileAllowed(["pdf", "jpg", "png", "jpeg"], "Apenas PDF e Imagens!")])
    documento_adicional = FileField("Documento Adicional (Opcional - PDF, Imagem, DOCX)", validators=[Optional(), FileAllowed(["pdf", "jpg", "png", "jpeg", "docx"], "Apenas PDF, Imagens ou DOCX!")])

    submit = SubmitField("Salvar Cliente Finalizado e Gerar Contrato")
