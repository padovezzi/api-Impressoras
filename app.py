from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Impressora, Manutencao
from datetime import datetime
import os

# Configuração do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///impressoras.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
CORS(app)

# Rota principal - Frontend
@app.route('/')
def index():
    return render_template('index.html')

# GET - Listar todas as impressoras
@app.route('/impressoras', methods=['GET'])
def get_impressoras():
    impressoras = Impressora.query.all()
    return jsonify([impressora.to_dict() for impressora in impressoras])

# GET - Buscar impressora por ID
@app.route('/impressoras/<int:id>', methods=['GET'])
def get_impressora(id):
    impressora = Impressora.query.get_or_404(id)
    return jsonify(impressora.to_dict())

# POST - Criar nova impressora
@app.route('/impressoras', methods=['POST'])
def create_impressora():
    data = request.get_json()
    
    # Verificar se já existe uma impressora com este patrimônio
    if Impressora.query.filter_by(PATRIMONIO=data['PATRIMONIO']).first():
        return jsonify({'erro': 'Já existe uma impressora com este número de patrimônio'}), 400
    
    impressora = Impressora(
        PATRIMONIO=data['PATRIMONIO'],
        FABRICANTE=data['FABRICANTE'],
        MODELO=data['MODELO'],
        TIPO=data['TIPO'],
        SUPRIMENTO=data['SUPRIMENTO'],
        PORTA=data['PORTA'],
        IP=data.get('IP', ''),
        MAC=data.get('MAC', ''),
        DEPARTAMENTO=data['DEPARTAMENTO'],
        ValorReferencia=data['ValorReferencia'],
        ALUGADA=data['ALUGADA'],
        UNIDADE=data['UNIDADE'],
        VOLTAGEM=data['VOLTAGEM'],
        STATUS=data['STATUS']
    )
    
    db.session.add(impressora)
    db.session.commit()
    
    return jsonify(impressora.to_dict()), 201

# PUT - Atualizar impressora
@app.route('/impressoras/<int:id>', methods=['PUT'])
def update_impressora(id):
    impressora = Impressora.query.get_or_404(id)
    data = request.get_json()
    
    # Verificar se o novo patrimônio já existe (se foi alterado)
    if 'PATRIMONIO' in data and data['PATRIMONIO'] != impressora.PATRIMONIO:
        if Impressora.query.filter_by(PATRIMONIO=data['PATRIMONIO']).first():
            return jsonify({'erro': 'Já existe uma impressora com este número de patrimônio'}), 400
    
    # Atualizar campos
    campos = ['PATRIMONIO', 'FABRICANTE', 'MODELO', 'TIPO', 'SUPRIMENTO', 'PORTA', 
              'IP', 'MAC', 'DEPARTAMENTO', 'ValorReferencia', 'ALUGADA', 'UNIDADE', 'VOLTAGEM', 'STATUS']
    
    for campo in campos:
        if campo in data:
            setattr(impressora, campo, data[campo])
    
    db.session.commit()
    
    return jsonify(impressora.to_dict())

# DELETE - Remover impressora
@app.route('/impressoras/<int:id>', methods=['DELETE'])
def delete_impressora(id):
    impressora = Impressora.query.get(id)

    if  not impressora:
        return jsonify({'erro': 'Impressora não encontrada'}), 404
    
    db.session.delete(impressora)
    db.session.commit()
    
    return jsonify({'mensagem': 'Impressora removida com sucesso'})


# GET - Buscar manutenções de uma impressora
@app.route('/impressoras/<int:id>/manutencoes', methods=['GET'])
def get_manutencoes_impressora(id):
    manutencoes = Manutencao.query.filter_by(impressora_id=id).all()
    return jsonify([manutencao.to_dict() for manutencao in manutencoes])

# POST - Adicionar manutenção a uma impressora
@app.route('/impressoras/<int:id>/manutencoes', methods=['POST'])
def add_manutencao_impressora(id):
    data = request.get_json()
    
    # Verificar se a impressora existe
    if not Impressora.query.get(id):
        return jsonify({'erro': 'Impressora não encontrada'}), 404
    
    # Converter string de data para objeto datetime, se necessário
    data_manutencao = datetime.utcnow()
    if 'data' in data and data['data']:
        try:
            data_manutencao = datetime.fromisoformat(data['data'].replace('Z', '+00:00'))
        except ValueError:
            pass
    
    manutencao = Manutencao(
        impressora_id=id,
        data=data_manutencao,
        valor=data['valor'],
        descricao=data['descricao'],
        tipo=data['tipo']
    )
    
    db.session.add(manutencao)
    db.session.commit()
    
    return jsonify(manutencao.to_dict()), 201

# GET - Listar todas as manutenções
@app.route('/impressoras/manutencoes', methods=['GET'])
def get_all_manutencoes():
    manutencoes = Manutencao.query.all()
    return jsonify([manutencao.to_dict() for manutencao in manutencoes])

if __name__ == '__main__':
    # Criar o banco de dados se não existir
    with app.app_context():
        db.create_all()
        print("Banco de dados verificado/criado com sucesso!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# DELETE FROM manutencao WHERE id IN (1, 2);