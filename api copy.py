from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'lucas_ulerich',
    'password': '1080',
    'database': 'fazenda'
}

# Função para conectar ao banco de dados
def connect_to_database():
    return mysql.connector.connect(**db_config)

# Rota para renderizar o formulário HTML
@app.route('/')
def index():
    return render_template('formulario.html')

# Rota para processar o formulário
@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if request.method == 'GET':
        plantacao = request.args.get('plantacao')
        data_fornecida = request.args.get('data', '')
    elif request.method == 'POST':
        data = request.json
        plantacao = data.get('plantacao')
        data_fornecida = data.get('data', '')

    if data_fornecida:
        data = datetime.strptime(data_fornecida, '%d-%m-%Y')
    else:
        data = datetime.now() - timedelta(days=1)

    data_inicio_str = data.strftime('%Y-%m-%d')

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(Quantidade_colheita) FROM Producao WHERE Plantacao = %s AND Data_plantacao = %s", (plantacao, data_inicio_str))
        total_colheita = cursor.fetchone()[0]

        # Determina a unidade de medida com base no tipo de plantação
        if 'cana' in plantacao.lower():
            unidade_medida = 'quilos'
        else:
            unidade_medida = 'sacas'

        conn.close()
        return jsonify({'data': data_inicio_str, 'plantacao': plantacao, 'total_colheita': total_colheita, 'unidade_medida': unidade_medida})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para consultar o banco de dados
@app.route('/consultar-banco-de-dados', methods=['GET', 'POST'])
def consultar_banco_de_dados():
    try:
        if request.method == 'GET':
            plantacao = request.args.get('plantacao')
            data_fornecida = request.args.get('data', '')
        elif request.method == 'POST':
            data = request.json
            plantacao = data.get('plantacao')
            data_fornecida = data.get('data', '')

        if data_fornecida:
            data = datetime.strptime(data_fornecida, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            data = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        data_inicio_str = data

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(Quantidade_colheita) FROM Producao WHERE Plantacao = %s AND Data_plantacao = %s", (plantacao, data_inicio_str))
        total_colheita = cursor.fetchone()[0]
        
        # Determina a unidade de medida com base no tipo de plantação
        if 'cana' in plantacao.lower():
            unidade_medida = 'quilos'
        else:
            unidade_medida = 'sacas'

        conn.close()

        return jsonify({'plantacao': plantacao, 'data': data_inicio_str, 'total_colheita': total_colheita, 'unidade_medida': unidade_medida})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
