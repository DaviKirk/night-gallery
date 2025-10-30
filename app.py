from flask import Flask, render_template, request, url_for, flash, redirect
import pymysql
import os
import uuid
from models.database import db, galleryPhoto

app = Flask(__name__, template_folder='views')

BD_NAME = 'photos_gallery'

app.config['DATABASE_NAME'] = BD_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:@localhost/{BD_NAME}?charset=utf8mb4"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in FILE_TYPES

@app.route('/', methods=['GET', 'POST'])
def gallery():
    
    photos = galleryPhoto.query.all()
    if request.method == 'POST':
        
        file = request.files['file']
        if not allowed_file(file.filename):
            flash('Tipo de arquivo não compativel(Permitidos: PNG, JPG, JPEG, GIF)', 'danger')
            return redirect(request.url)
        
        filename = str(uuid.uuid4())
        
        img = galleryPhoto(filename)
        db.session.add(img)
        db.session.commit()
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Foto enviada com sucesso!', 'success')
        return redirect(url_for('gallery'))
    
    return render_template('index.html')

if __name__ == '__main__':
    
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {BD_NAME}")
            print(f"Banco de dados '{BD_NAME}' verificado/criado com sucesso.")
            
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        connection.close()
        
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
            
    app.run(host="localhost", port=5000, debug=True)