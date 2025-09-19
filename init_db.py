from app import app, db
from models import Impressora, Manutencao

with app.app_context():
    # Criar todas as tabelas
    db.create_all()
    print("Banco de dados inicializado com sucesso!")
    print("Tabelas criadas: Impressora, Manutencao")