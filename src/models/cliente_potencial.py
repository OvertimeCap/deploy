from src import db  # Alterado para importação absoluta
from datetime import datetime

class ClientePotencial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=True) # Formato XXX.XXX.XXX-XX
    telefone = db.Column(db.String(20), nullable=True) # Formato (XX) XXXXX-XXXX
    email = db.Column(db.String(120), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    rg = db.Column(db.String(20), nullable=True)
    endereco_completo = db.Column(db.String(300), nullable=True)
    processo_judicial_numero = db.Column(db.String(100), nullable=True)
    vara_comarca = db.Column(db.String(150), nullable=True)
    
    valor_inscrito_requisitado = db.Column(db.Float, nullable=False, default=0.0)
    
    banco = db.Column(db.String(100), nullable=True)
    agencia = db.Column(db.String(20), nullable=True)
    conta_corrente = db.Column(db.String(30), nullable=True)
    
    status_interesse = db.Column(db.String(50), default="em negociação", nullable=False) # "em negociação", "sem interesse", "aguardando retorno"
    observacoes = db.Column(db.Text, nullable=True)
    data_primeiro_contato = db.Column(db.Date, default=datetime.utcnow)
    responsavel_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True) # Colaborador que cadastrou
    responsavel = db.relationship("User", backref=db.backref("clientes_potenciais_criados", lazy=True))

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def honorarios(self):
        return round(self.valor_inscrito_requisitado * 0.30, 2)

    @property
    def liquido_cliente(self):
        return round(self.valor_inscrito_requisitado - self.honorarios, 2)

    @property
    def proposta_70_pc(self):
        return round(self.liquido_cliente * 0.70, 2)

    def __repr__(self):
        return f"<ClientePotencial {self.nome_cliente}>"

