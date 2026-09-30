#!/usr/bin/env python3
"""Genera el sitio estático a partir de src/site.json, src/template.html
y los fragmentos de content/{en,es}/.

    python3 build.py

Salida: index.html + *.html en la raíz (inglés) y es/*.html (español).
"""
import json, os, re, html, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(f'{ROOT}/src/site.json', encoding='utf-8'))
TEMPLATE = open(f'{ROOT}/src/template.html', encoding='utf-8').read()
BASE_URL = 'https://www.kinolab07.co'

# Con --local, el botón "Ir a Lenguajeo" apunta al servidor local en vez de al
# dominio, para poder probar los dos sitios juntos sin conexión.
LOCAL = '--local' in sys.argv
LENGUAJEO_URL = SITE['lenguajeo_url_local'] if LOCAL else SITE['lenguajeo_url']

CHEV = ('<svg viewBox="0 0 10 6" aria-hidden="true" focusable="false">'
        '<path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" '
        'stroke-width="1.4"/></svg>')


def page_href(page):
    return 'index.html' if page == 'index' else f'{page}.html'


def all_pages(lang_cfg):
    """Toda página que aparece en el menú, en orden."""
    pages = []
    for item in lang_cfg['menu']:
        pages.append(item['page'])
        pages.extend(item.get('children', []))
    return pages


def read_content(lang, page):
    path = f'{ROOT}/content/{lang}/{page}.html'
    return open(path, encoding='utf-8').read() if os.path.exists(path) else None


def render_menu(lang_cfg, current, indent='                '):
    t = lang_cfg['titles']
    out = [f'{indent}<ul class="menu-primary-items">']
    for item in lang_cfg['menu']:
        page = item['page']
        kids = item.get('children', [])
        classes = ['menu-item']
        if kids:
            classes.append('menu-item-has-children')
        if page == current:
            classes.append('current-menu-item')
        aria = ' aria-current="page"' if page == current else ''
        out.append(f'{indent}  <li class="{" ".join(classes)}">')
        out.append(f'{indent}    <a href="{page_href(page)}"{aria}>'
                   f'{html.escape(t[page])}</a>')
        if kids:
            out.append(f'{indent}    <button class="toggle-dropdown" '
                       f'aria-expanded="false">'
                       f'<span class="screen-reader-text">'
                       f'{html.escape(lang_cfg["open_menu"])}</span>{CHEV}</button>')
            out.append(f'{indent}    <ul class="sub-menu">')
            for kid in kids:
                kc = 'menu-item current-menu-item' if kid == current else 'menu-item'
                ka = ' aria-current="page"' if kid == current else ''
                out.append(f'{indent}      <li class="{kc}">'
                           f'<a href="{page_href(kid)}"{ka}>'
                           f'{html.escape(t[kid])}</a></li>')
            out.append(f'{indent}    </ul>')
        out.append(f'{indent}  </li>')
    out.append(f'{indent}</ul>')
    return '\n'.join(out)


def render_lang_switch(lang, page, indent='              '):
    parts = []
    for code, cfg in SITE['languages'].items():
        label = html.escape(cfg['label'])
        if code == lang:
            parts.append(f'<span class="is-current" aria-current="true">{label}</span>')
        else:
            # cada idioma vive en su propia carpeta; el destino es la misma página
            if code == 'en':
                href = f'../{page_href(page)}'
            else:
                href = f'{cfg["dir"]}/{page_href(page)}'
            parts.append(f'<a href="{href}" hreflang="{cfg["html_lang"]}">{label}</a>')
    inner = '<span class="sep">/</span>'.join(parts)
    return (f'{indent}<nav class="lang-switch" aria-label="Idioma / Language">'
            f'{inner}</nav>')


def excerpt(content_html, limit=155):
    text = re.sub(r'<[^>]+>', ' ', content_html)
    text = html.unescape(re.sub(r'\s+', ' ', text)).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(' ', 1)[0] + '…'


def build_page(lang, page, lang_cfg):
    subdir = lang_cfg['dir']
    base = '' if not subdir else '../'
    title = lang_cfg['titles'][page]

    content = read_content(lang, page)
    if content is None:
        content = (f'<div class="pending-notice">\n'
                   f'  <p><strong>{html.escape(lang_cfg["pending_title"])}</strong></p>\n'
                   f'  <p>{html.escape(lang_cfg["pending_body"])}</p>\n'
                   f'</div>')
        pending = True
    else:
        pending = False

    # las rutas de assets en los fragmentos son relativas a la raíz del sitio
    content = content.replace('src="assets/', f'src="{base}assets/')
    content = content.replace('href="assets/', f'href="{base}assets/')
    content = content.replace('{{lenguajeo_url}}', LENGUAJEO_URL)

    head_title = (f'{SITE["site_title"]} – {SITE["tagline"]}' if page == 'index'
                  else f'{title} – {SITE["site_title"]}')

    url_path = ('' if not subdir else f'{subdir}/')
    canonical = (f'{BASE_URL}/{url_path}' if page == 'index'
                 else f'{BASE_URL}/{url_path}{page_href(page)}')

    alternates = []
    for code, cfg in SITE['languages'].items():
        p = '' if not cfg['dir'] else f'{cfg["dir"]}/'
        u = f'{BASE_URL}/{p}' if page == 'index' else f'{BASE_URL}/{p}{page_href(page)}'
        alternates.append(f'<link rel="alternate" hreflang="{cfg["html_lang"]}" href="{u}">')
    alternates.append(f'<link rel="alternate" hreflang="x-default" '
                      f'href="{BASE_URL}/{page_href(page) if page != "index" else ""}">')

    values = {
        'html_lang': lang_cfg['html_lang'],
        'lang': lang,
        'page': page,
        'head_title': html.escape(head_title),
        'description': html.escape(excerpt(content)),
        'canonical': canonical,
        'alternates': '\n'.join(alternates),
        'base': base,
        'home': 'index.html',
        'site_title': html.escape(SITE['site_title']),
        'tagline': html.escape(SITE['tagline']),
        'skip': html.escape(lang_cfg['skip']),
        'open_menu': html.escape(lang_cfg['open_menu']),
        'sidebar_label': html.escape(lang_cfg['sidebar_label']),
        'footer': html.escape(SITE['footer']),
        'title': html.escape(title),
        'menu': render_menu(lang_cfg, page),
        'lang_switch': render_lang_switch(lang, page),
        'content': content,
    }

    out = TEMPLATE
    for k, v in values.items():
        out = out.replace('{{' + k + '}}', v)

    leftovers = re.findall(r'\{\{(\w+)\}\}', out)
    if leftovers:
        sys.exit(f'marcador sin sustituir en {lang}/{page}: {set(leftovers)}')

    dest_dir = ROOT if not subdir else f'{ROOT}/{subdir}'
    os.makedirs(dest_dir, exist_ok=True)
    dest = f'{dest_dir}/{page_href(page)}'
    open(dest, 'w', encoding='utf-8').write(out)
    return dest, pending


def main():
    built, pendings = 0, []
    for lang, cfg in SITE['languages'].items():
        for page in all_pages(cfg):
            dest, pending = build_page(lang, page, cfg)
            built += 1
            if pending:
                pendings.append(os.path.relpath(dest, ROOT))
    print(f'{built} páginas generadas.')
    if LOCAL:
        print(f'Modo local: "Ir a Lenguajeo" apunta a {LENGUAJEO_URL}')
        print('Vuelve a ejecutar "python3 build.py" sin --local antes de publicar.')
    if pendings:
        print(f'{len(pendings)} sin contenido todavía:')
        for p in pendings:
            print('  -', p)


if __name__ == '__main__':
    main()
