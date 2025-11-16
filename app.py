# app.py
from flask import Flask, render_template
import markdown
import os
from datetime import datetime

app = Flask(__name__)

# Define la carpeta donde guardas tus archivos Markdown
MARKDOWN_DIR = 'markdown'

@app.route('/')
def inicio():
    # 1. Obtener la lista de archivos MD
    posts_files = os.listdir(MARKDOWN_DIR)
    
    posts_list = []
    
    for filename in posts_files:
        if filename.endswith('.md'):
            filepath = os.path.join(MARKDOWN_DIR, filename)
            
            # 2. Obtener el timestamp de modificación del archivo
            # St_mtime es el tiempo de la última modificación (timestamp UNIX)
            timestamp = os.path.getmtime(filepath)
            date_modified = datetime.fromtimestamp(timestamp)
            
            # 3. Leer el contenido y convertirlo a HTML (o solo un resumen si prefieres)
            with open(filepath, 'r', encoding='utf-8') as f:
                content_md = f.read()
                # Opcional: convertir a HTML aquí si no usas una BD
                content_html = markdown.markdown(content_md)

            # 4. Crear un diccionario con la información del post
            posts_list.append({
                'nombre': os.path.splitext(filename)[0], # Nombre del archivo sin .md
                'fecha': date_modified,
                'contenido_html': content_html # El contenido HTML completo para tu index.html
            })

    # 5. Ordenar la lista de diccionarios por la clave 'fecha' de forma descendente
    # reverse=True asegura que el más reciente (fecha mayor) vaya primero
    posts_ordenados = sorted(posts_list, key=lambda post: post['fecha'], reverse=True)
    
    # 6. Pasar la lista ordenada a la plantilla index.html
    return render_template('index.html', posts=posts_ordenados)

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')

# Mantienes esta ruta para ver posts individuales con el estilo que definiste
@app.route('/post/<nombre>')
def mostrar_post(nombre):
    ruta_md = os.path.join(MARKDOWN_DIR, f'{nombre}.md')
    if not os.path.exists(ruta_md):
        return "Post no encontrado", 404
    with open(ruta_md, 'r', encoding='utf-8') as f:
        contenido_md = f.read()
    contenido_html = markdown.markdown(contenido_md)
    # Usa tu plantilla index.html para mantener consistencia o la que prefieras
    return render_template_string("""
        <html>
        <head>
            <title>{{ nombre }}</title>
            <style>
                body {
                    background: #111;
                    color: #0f0;
                    font-family: monospace;
                    padding: 2em;
                }
                a { color: #0f0; }
                h1, h2, h3, h4, h5, h6 { color: #0f0; }
                hr { border: 1px solid #0f0; }
            </style>
        </head>
        <body>
            <a href="/">Volver a Inicio</a>
            {{ contenido|safe }}
        </body>
        </html>
    """, contenido=contenido_html, nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
