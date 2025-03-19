
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
    
#Search for Boat
@app.route('/boatsearch', methods = ["GET"])
def getBoatSearch():
    return render_template('boatsearch.html')

@app.route('/boatsearch', methods = ["POST"])
def searchBoat():
    boat_id = request.form['id']
    result = conn.execute(text("SELECT * FROM boats WHERE id = :id"), {"id": boat_id}).fetchone()
    if result:
        return render_template('boatsearch.html', boat=result, error=None, success="Your boat was found!")
    else:
        return render_template('boatsearch.html', boat=None, error="No boat found!", success=None)

#delete a boat: 

@app.route('/boatdelete', methods=["GET"])
def getDeleteBoat():
    return render_template('boatdelete.html')

@app.route('/boatdelete', methods=["POST"])
def deleteBoat():
    boat_id = request.form['id']
    result = conn.execute(text("DELETE FROM boats WHERE id = :id"), {"id": boat_id})
    conn.commit()
    if result.rowcount > 0:
        return render_template('boatdelete.html', error=None, success="Your boat was successfully deleted!")
    else:
        return render_template('boatdelete.html', error="Looks like we couldn't find your boat", success=None )

#Update a boat
@app.route('/boatupdate', methods=["GET", "POST"])
def getUpdateBoat():
    if request.method == "POST":  # Step 1: User submits their ID to fetch data
        boat_id = request.form.get('id')
        boat = conn.execute(
            text('SELECT * FROM boats WHERE id = :id'), {"id": boat_id}
        ).fetchone()
        
        if boat:
            return render_template('boatupdate.html', boat=boat, error=None, success=None)
        else:
            return render_template('boatupdate.html', boat=None, error="Boat not found.", success=None)
    else:  # Initial GET request renders empty form for user to enter ID
        return render_template('boatupdate.html', boat=None, error=None, success=None)


@app.route('/boatupdate/save', methods=["POST"])
def updateBoat():
    try:
        conn.execute(
            text('UPDATE boats SET name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price WHERE id = :id'),
            request.form
        )
        conn.commit()
        return render_template('boatupdate.html', error=None, success="Your boat was updated", boat=request.form)
    except:
        return render_template('boatupdate.html', error="Failed to update your boat.", success=None)

@app.route('/<name>')
def hello(name):
    return render_template('user.html', name = name)


if __name__ == '__main__':
    app.run(debug=True)