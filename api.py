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
@app.route('/consultar', methods=['GET'])
def consultar():
    plantacao = request.args.get('plantacao')
    dias = int(request.args.get('dias', 7))
    data_inicio = datetime.now() - timedelta(days=dias)
    data_inicio_str = data_inicio.strftime('%Y-%m-%d')

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(Quantidade_colheita) FROM Producao WHERE Plantacao = %s AND Data_plantacao >= %s", (plantacao, data_inicio_str))
        resultado = cursor.fetchone()[0]
        conn.close()
        return render_template('formulario.html', producao=resultado, plantacao=plantacao, dias=dias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Novo endpoint para a API
@app.route('/endpointAPI', methods=['GET', 'POST'])
def novo_endpoint():
    if request.method == 'GET':
        # Lógica para lidar com solicitações GET
        return jsonify({'message': 'GET request received'})
    elif request.method == 'POST':
        # Lógica para lidar com solicitações POST
        data = request.json  
        return jsonify({'message': 'POST request received', 'data': data})
    else:
        return jsonify({'error': 'Unsupported HTTP method'}), 405

if __name__ == '__main__':
    app.run(debug=True)
