from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app=Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitiowebconpythonyflask1'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    conexion=mysql.connect()
    print(conexion)
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():
    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/libros.html', libros=libros)

@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    _nombre=request.form['txtNombre']
    _archivo=request.files['txtImagen']
    _url=request.form['txtUrl']
    
    sql="INSERT INTO libros (id, nombre, imagen, url) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre, _archivo.filename, _url)
    
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    print(_nombre)
    print(_url)
    print(_archivo)
    return redirect('/admin/libros')

if __name__=='__main__':
    app.run(debug=True)