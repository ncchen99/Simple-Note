
import os
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = os.getenv('USER')
app.config["MYSQL_PASSWORD"] = os.getenv('PASSWORD')
app.config["MYSQL_DB"] = "note"

mysql = MySQL(app)


@app.route("/", methods=['POST', 'GET'])
def home():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        message = request.form['message']
        cur.execute(
            f"""INSERT INTO `note`.`note` (`message`) VALUES ('{message}')""")
        mysql.connection.commit()
    cur.execute("""SELECT id, message FROM `note`.`note`""")
    rv = cur.fetchall()
    data = [[rv[i][0], rv[i][1]] for i in range(len(rv))]
    return render_template('main.html', data=data)


@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(
        f"""DELETE FROM `note`.`note` WHERE id='{id}'""")
    mysql.connection.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()
