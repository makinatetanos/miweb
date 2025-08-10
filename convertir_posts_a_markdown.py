import os
import re
from bs4 import BeautifulSoup

# Asegúrate de tener BeautifulSoup instalado: pip install beautifulsoup4

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'post')
MARKDOWN_DIR = os.path.join(os.path.dirname(__file__), 'markdown')

if not os.path.exists(MARKDOWN_DIR):
    os.makedirs(MARKDOWN_DIR)

for filename in os.listdir(POSTS_DIR):
    if filename.endswith('.html'):
        html_path = os.path.join(POSTS_DIR, filename)
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Extraer título
        h2 = soup.find('h2')
        titulo = h2.get_text(strip=True) if h2 else ''

        # Extraer fecha
        fecha = ''
        fecha_span = soup.find('span', class_='fecha')
        if fecha_span:
            fecha = fecha_span.get_text(strip=True)

        # Extraer contenido principal (párrafos)
        contenido = ''
        section = soup.find('section', class_='post')
        if section:
            parrafos = section.find_all('p')
            contenido = '\n\n'.join(p.get_text(strip=True) for p in parrafos)

        # Extraer enlace de donación (si existe)
        donacion = ''
        donacion_a = soup.find('a', class_='boton-donacion')
        if donacion_a:
            url = donacion_a.get('href')
            texto = donacion_a.get_text(strip=True)
            donacion = f'[{texto}]({url})'

        # Construir el contenido Markdown
        md_lines = []
        if titulo:
            md_lines.append(f'# {titulo}\n')
        if fecha:
            md_lines.append(f'*{fecha}*\n')
        if contenido:
            md_lines.append(contenido + '\n')
        if donacion:
            md_lines.append(f'\n---\n\n{donacion}\n')

        md_content = '\n'.join(md_lines)

        # Guardar archivo Markdown
        md_filename = os.path.splitext(filename)[0] + '.md'
        md_path = os.path.join(MARKDOWN_DIR, md_filename)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

print('Conversión completada. Los archivos Markdown están en la carpeta markdown/.')