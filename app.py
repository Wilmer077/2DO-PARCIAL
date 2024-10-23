from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

@app.before_request
def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    return render_template('index.html', productos=session['productos'])


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        if 'contador_productos' not in session:
            session['contador_productos'] = 1
        else:
            session['contador_productos'] += 1

        id_producto = session['contador_productos'] 
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        nuevo = {
            'id': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        session['productos'].append(nuevo)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')


@app.route('/eliminar_producto/<id_producto>')
def eliminar_producto(id_producto):
    session['productos'] = [producto for producto in session['productos'] if producto['id'] != int(id_producto)]
    session.modified = True
    return redirect(url_for('index'))


@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar(id_producto):
    producto = next((prod for prod in session['productos'] if prod['id'] == id_producto), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)