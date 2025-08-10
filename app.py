from flask import Flask, render_template, render_template_string
import markdown
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')

@app.route('/post/<nombre>')
def mostrar_post(nombre):
    ruta_md = os.path.join('markdown', f'{nombre}.md')
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