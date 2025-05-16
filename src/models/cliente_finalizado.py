from src import db  # Alterado para importação absoluta
from datetime import datetime

class ClienteFinalizado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Campos baseados na análise do cadastros.ods
    cliente_nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True) # CPF deve ser único para finalizados
    numero_processo = db.Column(db.String(100), nullable=True)
    vara = db.Column(db.String(150), nullable=True)
    precatorio = db.Column(db.String(100), nullable=True)
    n_cnj = db.Column(db.String(100), nullable=True, name="n_cnj") # nome da coluna no ODS é Nº CNJ
    of_requisitorio = db.Column(db.String(100), nullable=True, name="of_requisitorio")
    percentual_cessao = db.Column(db.Float, nullable=True)
    ano_previsto_pagamento = db.Column(db.Integer, nullable=True)
    preco_aquisicao = db.Column(db.Float, nullable=True)
    data_calculo = db.Column(db.Date, nullable=True)
    data_compra = db.Column(db.Date, nullable=True)
    local_compra = db.Column(db.String(150), nullable=True, name="local") # nome da coluna no ODS é LOCAL
    data_pagamento_cliente = db.Column(db.Date, nullable=True, name="data_do_pagamento") # nome da coluna no ODS é DATA DO PAGAMENTO
    
    valor_inscrito_requisitado = db.Column(db.Float, nullable=True)
    honorarios_contratuais = db.Column(db.Float, nullable=True, name="honorarios") # nome da coluna no ODS é Honorários
    liquido_comprado = db.Column(db.Float, nullable=True)
    
    resultado_esperado = db.Column(db.Float, nullable=True)
    percentual_ganho = db.Column(db.Float, nullable=True)
    valor_depositado_judicial = db.Column(db.Float, nullable=True, name="valor_depositado") # nome da coluna no ODS é VALOR DEPOSITADO
    liquido_a_levantar = db.Column(db.Float, nullable=True)
    numero_conta_judicial = db.Column(db.String(50), nullable=True, name="numero_da_conta") # nome da coluna no ODS é NÚMERO DA CONTA
    data_alvara = db.Column(db.Date, nullable=True)
    valor_recebido_empresa = db.Column(db.Float, nullable=True, name="valor_recebido") # nome da coluna no ODS é VALOR RECEBIDO
    data_recebimento_empresa = db.Column(db.Date, nullable=True, name="data_do_recebimento") # nome da coluna no ODS é DATA DO RECEBIMENTO
    resultado_final = db.Column(db.Float, nullable=True)
    tributacao = db.Column(db.String(100), nullable=True)
    banco_cliente = db.Column(db.String(100), nullable=True, name="banco") # nome da coluna no ODS é BANCO
    
    # Campos para o Painel de Tarefas
    status_tarefa = db.Column(db.String(50), default="aguardando documentos", nullable=False) 
    # Exemplos de status: "aguardando documentos", "contrato gerado", "documentos assinados", "pagamento efetuado", "finalizado"
    observacao = db.Column(db.Text, nullable=True) # Mantido como observacao, pois é o nome no form e no ODS.

    # Campos para upload de arquivos
    documento_rg_cnh_path = db.Column(db.String(300), nullable=True)
    comprovante_endereco_path = db.Column(db.String(300), nullable=True)
    comprovante_pagamento_path = db.Column(db.String(300), nullable=True)
    documento_adicional_path = db.Column(db.String(300), nullable=True)

    # Relacionamento com o usuário (colaborador que cadastrou/responsável pela tarefa)
    responsavel_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    responsavel = db.relationship("User", backref=db.backref("tarefas_atribuidas", lazy=True))

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ClienteFinalizado {self.cliente_nome} - {self.cpf}>"

