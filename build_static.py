import os
import shutil
from pathlib import Path

import markdown as md
from jinja2 import Environment, FileSystemLoader


PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"
MARKDOWN_DIR = PROJECT_ROOT / "markdown"
OUTPUT_DIR = PROJECT_ROOT / "docs"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_static() -> None:
    dest = OUTPUT_DIR / "static"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(STATIC_DIR, dest)


def make_nojekyll() -> None:
    (OUTPUT_DIR / ".nojekyll").write_text("")


def build_pages(env: Environment) -> None:
    # Utilidad de url_for para plantillas estáticas
    def url_for(endpoint: str, **values) -> str:
        if endpoint == "static":
            filename = values.get("filename", "")
            return f"static/{filename}"
        if endpoint == "proyectos":
            return "proyectos.html"
        if endpoint == "contacto":
            return "contacto.html"
        if endpoint == "mostrar_post":
            nombre = values.get("nombre")
            return f"posts/{nombre}.html"
        if endpoint == "inicio":
            return "index.html"
        # Fallback
        return "#"

    context = {"url_for": url_for}

    # Render páginas principales
    for template_name in ["index.html", "proyectos.html", "contacto.html"]:
        template = env.get_template(template_name)
        html = template.render(**context)
        (OUTPUT_DIR / template_name).write_text(html, encoding="utf-8")


def build_posts() -> None:
    posts_out = OUTPUT_DIR / "posts"
    ensure_dir(posts_out)

    for md_file in sorted(MARKDOWN_DIR.glob("*.md")):
        nombre = md_file.stem
        contenido_md = md_file.read_text(encoding="utf-8")
        contenido_html = md.markdown(contenido_md)

        page_html = f"""
<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{nombre}</title>
  <style>
    body {{
      background: #111;
      color: #0f0;
      font-family: monospace;
      padding: 2em;
      line-height: 1.6;
    }}
    a {{ color: #0f0; }}
    h1, h2, h3, h4, h5, h6 {{ color: #0f0; }}
    hr {{ border: 1px solid #0f0; }}
  </style>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
  <link rel=\"stylesheet\" href=\"../static/styles.css\" />
  <link rel=\"icon\" href=\"data:,\" />
  <meta name=\"robots\" content=\"noindex\" />
  </head>
<body>
  {contenido_html}
</body>
</html>
"""
        (posts_out / f"{nombre}.html").write_text(page_html, encoding="utf-8")


def main() -> None:
    ensure_dir(OUTPUT_DIR)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    copy_static()
    make_nojekyll()
    build_pages(env)
    build_posts()
    print(f"Sitio estático generado en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()


