from flask import Flask, render_template, request,redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


#MySql COnnection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)


app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data =  cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods={'POST'})
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
                    (fullname, phone, email))
        mysql.connection.commit()    
        flash('Contact Added Succesfully')   
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE idcontacts = %s',[id])
    data =  cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])


@app.route('/update/<id>', methods = ['POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            phone = %s,
            email = %s
        WHERE idcontacts = %s
        """, (fullname, phone , email,id))
        mysql.connection.commit()   
        flash('Contact update Succesfully')   
        return redirect(url_for('index'))
 

@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts where idcontacts = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Removido')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)