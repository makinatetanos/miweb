# app.py
from flask import Flask, render_template
import markdown
import os
import glob # Necesitamos glob para encontrar archivos que terminen en .md

app = Flask(__name__)
# Asegúrate de que el directorio 'markdown' exista
MARKDOWN_DIR = 'markdown'
if not os.path.exists(MARKDOWN_DIR):
    os.makedirs(MARKDOWN_DIR)

@app.route('/')
def inicio():
    # 1. Obtener la lista de rutas completas de todos los archivos .md
    rutas_archivos = glob.glob(os.path.join(MARKDOWN_DIR, '*.md'))
    
    # 2. Crear una lista de diccionarios, incluyendo la fecha de modificación
    # os.path.getmtime(ruta) devuelve la fecha de modificación (timestamp numérico)
    posts_con_fechas = []
    for ruta in rutas_archivos:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido_md = f.read()
        
        # Convertimos el MD a HTML aquí mismo para simplificar la plantilla
        contenido_html = markdown.markdown(contenido_md)
        
        posts_con_fechas.append({
            'fecha_modificacion': os.path.getmtime(ruta),
            'contenido_html': contenido_html,
            'nombre_archivo': os.path.basename(ruta).replace('.md', '')
        })

    # 3. Ordenar la lista por 'fecha_modificacion' de forma descendente (más reciente primero)
    # reverse=True hace que sea de mayor a menor (más nuevo a más antiguo)
    posts_ordenados = sorted(posts_con_fechas, key=lambda post: post['fecha_modificacion'], reverse=True)
    
    # 4. Pasar la lista ordenada a la plantilla
    return render_template('index.html', posts=posts_ordenados)

# ... (El resto de tus rutas: contacto, proyectos, mostrar_post) ...
@app.route('/contacto')
def contacto():
    # ...
    return render_template('contacto.html')

@app.route('/proyectos')
def proyectos():
    # ...
    return render_template('proyectos.html')

@app.route('/post/<nombre>')
def mostrar_post(nombre):
    # Esta ruta ya estaba bien para mostrar posts individuales
    ruta_md = os.path.join('markdown', f'{nombre}.md')
    # ... (resto de la lógica de mostrar_post) ...
    if not os.path.exists(ruta_md):
        return "Post no encontrado", 404
    with open(ruta_md, 'r', encoding='utf-8') as f:
        contenido_md = f.read()
    contenido_html = markdown.markdown(contenido_md)
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
            {{ contenido|safe }}
        </body>
        </html>
    """, contenido=contenido_html, nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
