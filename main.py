
from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__) 
#connection string is in the format mysql://user:password@server/database

conn_str = "mysql://root:cset155@localhost/boatsdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def greeting():
    return render_template('index.html')

@app.route('/boats')
def boats():
    boats = conn.execute(text( 'select * from boats')).all()
    for boat in boats:
        print(boat[0])
    return render_template('boats.html', boats = boats[:10])

@app.route('/boatcreate', methods = ["GET"])
def getBoat():
    return render_template('boat_create.html')


@app.route('/boatcreate', methods = ["POST"])
def createBoat():
    try:
        conn.execute(text('insert into boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form)
        return render_template('boat_create.html',error = None, success = "Successful")
    except:
        return render_template('boat_create.html', error = "failed", success = None)
@app.route('/<name>')
def hello(name):
    return render_template('user.html', name = name)

'''
@app.route('/hello')
def hello():
    return "Hello"


@app.route('/hello/<int:name>')
def serveCoffee(name):
    return f"The next number is,  {name + 1}"

@app.route('/donut')
def serveDonut():
    return "Here is your donut."
    '''

if __name__ == '__main__':
    app.run(debug=True)