from flask import Flask, request, jsonify
import mysql.connector

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

# Rota para consultar o banco de dados
@app.route('/consultar-banco-de-dados', methods=['GET', 'POST'])
def consultar_banco_de_dados():
    try:
        if request.method == 'GET':
            opcao = request.args.get('Opcoes')
        elif request.method == 'POST':
            data = request.json
            opcao = data.get('Opcoes')
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT Volume FROM Producao WHERE Opcoes = %s", (opcao,))
        volume = cursor.fetchone()
        conn.close()

        if volume:
            # Alterando a forma como a opção é exibida
            opcao_formatada = opcao.replace('últimos', '- Últimos')
            # Formatando o volume com separadores de milhar e sem casas decimais
            volume_formatado = '{:,.0f}'.format(float(volume[0])).replace(',', '.')
            # Adicionando a unidade "toneladas" ao volume
            volume_com_unidade = "{} toneladas".format(volume_formatado)
            return jsonify({'opcao': opcao_formatada, 'volume': volume_com_unidade})
        else:
            return jsonify({'error': 'Opcao nao encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
