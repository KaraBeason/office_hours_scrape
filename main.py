from flask import Flask, json, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySql configs
app.config['MYSQL_DATABASE_USER'] = 'kara'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'OfficeHours'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route('/')
def main():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * from tbl_user where status = 'in';"
        cursor.execute(query)
        conn.commit()
        data = cursor.fetchall()
    except Exception as e:
        return json.dumps({'error': str(e)})

    finally:
        cursor.close()
        conn.close()
    return render_template('index.html', data=data)


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'html': '<span>Information validated.</span>'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter required information.</span'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/showMathDep')
def showMathDep():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * from tbl_user where department = 'math';"
        cursor.execute(query)
        conn.commit()
        data = cursor.fetchall()
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()
    return render_template('showMathDep.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
