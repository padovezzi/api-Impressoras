from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Impressora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PATRIMONIO = db.Column(db.Integer, unique=False, nullable=False)
    FABRICANTE = db.Column(db.String(100), nullable=False)
    MODELO = db.Column(db.String(100), nullable=False)
    TIPO = db.Column(db.String(50), nullable=False)
    SUPRIMENTO = db.Column(db.String(50), nullable=False)
    PORTA = db.Column(db.String(50), nullable=False)
    IP = db.Column(db.String(50), default="")
    MAC = db.Column(db.String(50), default="")
    DEPARTAMENTO = db.Column(db.String(100), nullable=False)
    ValorReferencia = db.Column(db.Float, nullable=False)
    ALUGADA = db.Column(db.String(10), nullable=False)
    UNIDADE = db.Column(db.String(100), nullable=False)
    VOLTAGEM = db.Column(db.String(50), nullable=False)
    STATUS = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'PATRIMONIO': self.PATRIMONIO,
            'FABRICANTE': self.FABRICANTE,
            'MODELO': self.MODELO,
            'TIPO': self.TIPO,
            'SUPRIMENTO': self.SUPRIMENTO,
            'PORTA': self.PORTA,
            'IP': self.IP,
            'MAC': self.MAC,
            'DEPARTAMENTO': self.DEPARTAMENTO,
            'ValorReferencia': self.ValorReferencia,
            'ALUGADA': self.ALUGADA,
            'UNIDADE': self.UNIDADE,
            'VOLTAGEM': self.VOLTAGEM,
            'STATUS': self.STATUS,
            'data_criacao': self.data_criacao.isoformat()
        }

class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    impressora_id = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'impressora_id': self.impressora_id,
            'data': self.data.isoformat(),
            'valor': self.valor,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'data_criacao': self.data_criacao.isoformat()
        }