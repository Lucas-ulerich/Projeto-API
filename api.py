from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'LucasUlerich.mysql.pythonanywhere-services.com',
    'user': 'LucasUlerich',
    'password': 'godofwar3',
    'database': 'LucasUlerich$FazendaDB'
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
        dias = int(request.args.get('dias', 7))
    elif request.method == 'POST':
        data = request.json
        plantacao = data.get('plantacao')
        dias = data.get('dias')

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

# Endpoint para consultar o banco de dados
@app.route('/consultar-banco-de-dados', methods=['GET', 'POST'])
def consultar_banco_de_dados():
    if request.method == 'GET':
        try:
            plantacao = request.args.get('plantacao')
            dias = int(request.args.get('dias', 7))
            data_inicio = datetime.now() - timedelta(days=dias)
            data_inicio_str = data_inicio.strftime('%Y-%m-%d')

            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(Quantidade_colheita) FROM Producao WHERE Plantacao = %s AND Data_plantacao >= %s", (plantacao, data_inicio_str))
            total_colheita = cursor.fetchone()[0]
            conn.close()

            return jsonify({'plantacao': plantacao, 'dias': dias, 'total_colheita': total_colheita})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            plantacao = data.get('plantacao')
            dias = int(data.get('dias', 7))
            data_inicio = datetime.now() - timedelta(days=dias)
            data_inicio_str = data_inicio.strftime('%Y-%m-%d')

            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(Quantidade_colheita) FROM Producao WHERE Plantacao = %s AND Data_plantacao >= %s", (plantacao, data_inicio_str))
            total_colheita = cursor.fetchone()[0]
            conn.close()

            return jsonify({'plantacao': plantacao, 'dias': dias, 'total_colheita': total_colheita})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
