import sqlite3
from flask import Flask, render_template, request


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, addr TEXT, '
                 'city TEXT, pin TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)


@app.route('/')
@app.route('/enter-new/')
def enter_new_student():
    return render_template('student.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        try:
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, addr, city, pin) VALUES (?,?,?,?)", (name, addr, city, pin))
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation" + e
        finally:
            con.close()
            return render_template('result.html', msg=msg)


@app.route('/show-records/', methods=['GET'])
def show_redords():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM students")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return render_template('records.html', records=records)


@app.route('/delete-student/<int:student_id>/', methods=["GET"])
def delete_student(student_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE id=" + str(student_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return render_template('delete-success.html', msg=msg)
