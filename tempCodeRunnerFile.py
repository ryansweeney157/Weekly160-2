
@app.route('/hello/<int:name>')
def serveCoffee(name):
    return f"Hello, {name}"