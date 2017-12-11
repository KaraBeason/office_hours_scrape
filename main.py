from flask import *
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


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/showSignIn')
def showSignIn():
    return render_template('signIn.html')


@app.route('/signIn', methods=['POST'])
def signIn():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        if _email and _password:
            # cursor.callproc('sp_createUser', (_accountType, _name, _email, _password))
            cursor.execute("select * from tbl_user where user_id = %s and password = %s", (_email, _password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect(url_for('dashboard'))
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>User not found.</span'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _accountType = request.form['accountType']
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        if _name and _email and _password:
            cursor.callproc('sp_createUser', (_accountType, _name, _email, _password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect(url_for('dashboard'))
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
