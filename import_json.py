import json
from app import app, db
from models import Impressora
from datetime import datetime

def importar_impressoras(json_file_path):
    with app.app_context():
        try:
            # Ler o arquivo JSON
            with open(json_file_path, 'r', encoding='utf-8') as file:
                impressoras_data = json.load(file)
            
            print(f"Encontradas {len(impressoras_data)} impressoras no JSON")
            
            contador = 0
            impressoras_duplicadas = 0
            
            for data in impressoras_data:
                # Verificar se já existe uma impressora com este patrimônio
                #if Impressora.query.filter_by(PATRIMONIO=data['PATRIMONIO']).first():
                #   print(f"Impressora com patrimônio {data['PATRIMONIO']} já existe. Pulando...")
                #    impressoras_duplicadas += 1
                #    continue
                
                # Criar nova impressora
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
                contador += 1
                
                # Commitar a cada 10 registros para melhor performance
                if contador % 10 == 0:
                    db.session.commit()
                    print(f"Importadas {contador} impressoras...")
            
            # Commitar quaisquer registros restantes
            db.session.commit()
            
            print(f"✅ Importação concluída!")
            print(f"📊 Total importado: {contador} impressoras")
            print(f"🚫 Impressoras duplicadas (não importadas): {impressoras_duplicadas}")
            
        except Exception as e:
            print(f"❌ Erro durante a importação: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    # Caminho para seu arquivo JSON
    caminho_json = 'arquivo.json'  # Altere para o nome do seu arquivo
    
    print("Iniciando importação de impressoras...")
    importar_impressoras(caminho_json)