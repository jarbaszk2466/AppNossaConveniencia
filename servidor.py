from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def iniciar_banco():
    conn = sqlite3.connect('estoque_central.db')
    # Adicionamos 'rowid' que é um ID automático do SQLite
    conn.execute('''CREATE TABLE IF NOT EXISTS estoque 
                    (produto TEXT, vencimento TEXT, alerta TEXT)''')
    conn.close()

@app.route('/adicionar', methods=['POST'])
def adicionar():
    dados = request.json
    conn = sqlite3.connect('estoque_central.db')
    conn.execute("INSERT INTO estoque VALUES (?, ?, ?)", 
                 (dados['produto'], dados['vencimento'], dados['alerta']))
    conn.commit()
    conn.close()
    return {"status": "sucesso"}, 200

@app.route('/listar', methods=['GET'])
def listar():
    conn = sqlite3.connect('estoque_central.db')
    # Pegamos o 'rowid' para saber qual item apagar depois
    cursor = conn.execute("SELECT rowid, * FROM estoque ORDER BY alerta ASC")
    itens = [{"id": row[0], "produto": row[1], "vencimento": row[2], "alerta": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(itens)

@app.route('/apagar_item/<int:item_id>', methods=['DELETE'])
def apagar_item(item_id):
    conn = sqlite3.connect('estoque_central.db')
    conn.execute("DELETE FROM estoque WHERE rowid = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "item apagado"}, 200

if __name__ == '__main__':
    iniciar_banco()
    print("SERVIDOR ONLINE: http://192.168.1.86:5000")
    app.run(host='0.0.0.0', port=5000)