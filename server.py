from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Создаем таблицу в базе данных SQLite
def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        date TEXT,
        time TEXT,
        click_number INTEGER)''')
    conn.commit()
    conn.close()

create_table()

# Обработчик POST запроса на добавление данных в таблицу
@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (text, date, time, click_number) VALUES (?, ?, ?, ?)',
                   (data['text'], data['date'], data['time'], data['click_number']))
    conn.commit()
    conn.close()
    return 'Данные успешно добавлены'

# Обработчик GET запроса на получение всех данных из таблицы
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append({'id': row[0], 'text': row[1], 'date': row[2], 'time': row[3], 'click_number': row[4]})
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
