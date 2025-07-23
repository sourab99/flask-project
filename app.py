from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'devproject_flask'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/view')

@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return render_template('view_data.html', users=data)


@app.route('/edit/<int:id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    return render_template('edit.html', user=user)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view'))

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view'))

if __name__ == '__main__':
    app.run(debug=True)
