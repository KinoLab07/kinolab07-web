#!/usr/bin/env python3
"""Convierte el HTML de bloques de WordPress (reference/pages.json)
en fragmentos HTML limpios dentro de content/{en,es}/."""
import json, os, re, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_MAP = json.load(open(f'{ROOT}/reference/image-map.json'))
# nombre de archivo original -> nombre nuevo (sin carpeta de año)
BY_BASENAME = {os.path.basename(k): v for k, v in IMG_MAP.items()}

# slug de WordPress -> página del sitio nuevo
PAGE_OF_SLUG = {
    'news': 'index', 'biography': 'biography', 'cv-en': 'cv', 'filmmaker': 'filmmaker',
    'walking_language': 'walking-language', 'aletheia-2-2': 'aletheia',
    'photography': 'photography', 'memories-of-san-pedro': 'memories-of-san-pedro',
    'memories-of-san-pedro-ii': 'memories-of-san-pedro-ii', 'plastic-art': 'plastic-art',
    'light-messages': 'light-messages',
    'news-espanol': 'index', 'biografia': 'biography', 'cv': 'cv',
    'cinematografia': 'filmmaker', 'lenguajeo-3': 'walking-language',
    'a-laube-2': 'a-laube', 'fotografias-2': 'photography',
    'memorias-del-san-pedro': 'memories-of-san-pedro',
    'memorias-del-san-pedro-ii-2': 'memories-of-san-pedro-ii',
    'artes-plasticas': 'plastic-art', 'mensajes-de-luz-2': 'light-messages',
}
LANG_OF_SLUG = {
    'news': 'en', 'biography': 'en', 'cv-en': 'en', 'filmmaker': 'en',
    'walking_language': 'en', 'aletheia-2-2': 'en', 'photography': 'en',
    'memories-of-san-pedro': 'en', 'memories-of-san-pedro-ii': 'en',
    'plastic-art': 'en', 'light-messages': 'en',
    'news-espanol': 'es', 'biografia': 'es', 'cv': 'es', 'cinematografia': 'es',
    'lenguajeo-3': 'es', 'a-laube-2': 'es', 'fotografias-2': 'es',
    'memorias-del-san-pedro': 'es', 'memorias-del-san-pedro-ii-2': 'es',
    'artes-plasticas': 'es', 'mensajes-de-luz-2': 'es',
}
# enlaces internos del contenido -> página destino
LINK_TO_PAGE = {
    'walking_language': 'walking-language', 'lenguajeo-3': 'walking-language',
    'aletheia-2': 'aletheia', 'aletheia-2-2': 'aletheia', 'aletheia-4': 'aletheia',
    'euritmia-2': 'euritmia', 'euritmia-3': 'euritmia',
    'the-story': 'the-story', 'el-cuento': 'the-story', 'el-cuento-4': 'the-story',
    'at-dawn': 'a-laube', 'a-laube': 'a-laube', 'a-laube-2': 'a-laube',
    'monica': 'monica', 'monica-2': 'monica', 'monica-4': 'monica',
    'sipar': 'sipar', 'sipar-2': 'sipar', 'sipar-4': 'sipar',
    'game': 'game', 'juego': 'game', 'gioco': 'game', 'gioco-2': 'game',
    'light-messages': 'light-messages', 'mensajes-de-luz-2': 'light-messages',
    'memories-of-san-pedro': 'memories-of-san-pedro',
    'memories-of-san-pedro-ii': 'memories-of-san-pedro-ii',
    'memorias-del-san-pedro': 'memories-of-san-pedro',
    'memorias-del-san-pedro-ii-2': 'memories-of-san-pedro-ii',
    'biography': 'biography', 'biografia': 'biography', 'filmmaker': 'filmmaker',
    'cinematografia': 'filmmaker', 'photography': 'photography',
    'fotografias-2': 'photography', 'plastic-art': 'plastic-art',
    'artes-plasticas': 'plastic-art', 'cv-en': 'cv', 'cv': 'cv',
}
PAGE_ID_TO_PAGE = {  # los ?page_id= que aún aparecen en el contenido
    '279': 'memories-of-san-pedro', '327': 'memories-of-san-pedro-ii',
    '482': 'euritmia', '461': 'the-story', '525': 'at-dawn',
    '719': 'monica', '420': 'sipar', '193': 'game', '672': 'a-laube',
}

def display_size(src, new_name):
    """Dimensiones a las que WordPress mostraba la imagen.

    WordPress servía versiones redimensionadas (`foo-189x1024.jpg`) y aquí
    guardamos siempre el original, que puede ser mucho mayor. Sin declarar el
    tamaño que tenía la variante, el navegador maquetaría con otra escala.
    """
    base = html.unescape(os.path.basename(src.split('?')[0]))
    m = re.search(r'-(\d+)x(\d+)\.[A-Za-z]+$', base)
    if m:
        return int(m.group(1)), int(m.group(2))
    with Image.open(f'{ROOT}/assets/images/{new_name}') as im:
        return im.size


def local_image(src):
    base = os.path.basename(src.split('?')[0])
    base = html.unescape(base)
    # quita el sufijo de tamaño que añade WordPress: foo-1024x335.jpg
    orig = re.sub(r'-\d+x\d+(\.[A-Za-z]+)$', r'\1', base)
    new = BY_BASENAME.get(orig) or BY_BASENAME.get(base)
    if not new:
        raise SystemExit(f'imagen sin mapear: {src}')
    return new

def local_link(href, lang):
    href = html.unescape(href)
    if 'kinolab07.co' not in href:
        return href
    if 'lenguajeo.kinolab07.co' in href:
        return href
    m = re.search(r'page_id=(\d+)', href)
    page = PAGE_ID_TO_PAGE.get(m.group(1)) if m else None
    if not page:
        slug = href.rstrip('/').split('/')[-1].split('?')[0]
        page = LINK_TO_PAGE.get(slug)
    if not page:
        return href
    if page == 'index':
        return '.' if lang == 'en' else '.'
    return f'{page}.html'

CLASS_MAP = {
    'aligncenter': 'align-center', 'alignwide': 'align-wide',
    'alignfull': 'align-full', 'alignleft': 'align-left',
    'alignright': 'align-right', 'has-text-align-center': 'center',
    'has-text-align-left': 'left', 'has-text-align-right': 'right',
    'has-regular-font-size': 'fs-regular', 'has-large-font-size': 'fs-large',
    'has-larger-font-size': 'fs-larger', 'has-small-font-size': 'fs-small',
    'has-medium-font-size': 'fs-medium', 'is-style-wide': 'wide',
    'is-vertically-aligned-center': 'v-center', 'is-vertically-aligned-top': 'v-top',
}
DROP_CLASS_RE = re.compile(
    r'^(wp-image-\d+|wp-block-[\w-]*|wp-element-caption|wp-container-[\w-]*|'
    r'is-layout-\w+|is-resized|is-light|is-provider-\w+|is-type-\w+|size-\w+|'
    r'has-(css-opacity|background-dim(-\d+)?|text-color|background|'
    r'\w+-color|\w+-background-color)|wp-has-aspect-ratio|wp-embed-aspect-\d+-\d+)$')

def clean_classes(value):
    out = []
    for c in value.split():
        if c in CLASS_MAP:
            out.append(CLASS_MAP[c])
        elif not DROP_CLASS_RE.match(c):
            out.append(c)
    seen, res = set(), []
    for c in out:
        if c not in seen:
            seen.add(c); res.append(c)
    return ' '.join(res)


def convert(content, lang):
    c = content

    # --- embeds de Vimeo -> iframe responsivo propio ---
    def embed(m):
        vid = re.search(r'vimeo\.com/(?:video/)?(\d+)', m.group(0))
        if not vid:
            return ''
        return (f'<div class="video">'
                f'<iframe src="https://player.vimeo.com/video/{vid.group(1)}?dnt=1" '
                f'title="Vimeo" loading="lazy" allow="fullscreen; picture-in-picture" '
                f'allowfullscreen></iframe></div>')
    c = re.sub(r'<figure class="wp-block-embed[^"]*".*?</figure>', embed, c, flags=re.S)

    # --- wp-block-cover -> separador vertical, conservando su contenido ---
    def cover(m):
        h = re.search(r'min-height:\s*(\d+)px', m.group(0))
        inner = re.search(r'wp-block-cover__inner-container[^"]*"[^>]*>(.*?)</div>',
                          m.group(0), re.S)
        body = inner.group(1) if inner else ' '
        return (f'<div class="spacer" style="min-height:{h.group(1) if h else 50}px">'
                f'<div>{body}</div></div>')
    c = re.sub(r'<div class="wp-block-cover[^"]*"[^>]*>.*?</div>\s*</div>',
               cover, c, flags=re.S)

    # --- columnas ---
    c = re.sub(r'<div class="[^"]*wp-block-columns[^"]*"([^>]*)>',
               lambda m: '<div class="cols"' + style_attr(m.group(1)) + '>', c)
    c = re.sub(r'<div class="[^"]*wp-block-column\b[^"]*"([^>]*)>',
               lambda m: '<div class="col' + extra_col(m.group(0)) + '"'
                         + style_attr(m.group(1)) + '>', c)
    # --- grupos: se descartan los envoltorios ---
    c = re.sub(r'<div class="[^"]*wp-block-group[^"]*"[^>]*>', '<div>', c)
    # --- envoltorio div.wp-block-image alrededor de una figure: sobra ---
    c = re.sub(r'<div class="wp-block-image">\s*(<figure.*?</figure>)\s*</div>',
               r'\1', c, flags=re.S)

    # --- imágenes ---
    def img(m):
        a = m.group(1)
        src = re.search(r'src="([^"]+)"', a)
        cls = re.search(r'class="([^"]*)"', a)
        alt = re.search(r'alt="([^"]*)"', a)
        st  = re.search(r'style="([^"]*)"', a)
        w   = re.search(r'width="(\d+)"', a)
        h   = re.search(r'height="(\d+)"', a)
        name = local_image(src.group(1))
        parts = [f'src="assets/images/{name}"']
        parts.append(f'alt="{alt.group(1) if alt else ""}"')
        if w and h:
            parts.append(f'width="{w.group(1)}" height="{h.group(1)}"')
        else:
            dw, dh = display_size(src.group(1), name)
            parts.append(f'width="{dw}" height="{dh}"')
        if st:
            s = re.sub(r'aspect-ratio:[^;]*;?', '', st.group(1)).strip()
            if s: parts.append(f'style="{s}"')
        cc = clean_classes(cls.group(1)) if cls else ''
        if cc: parts.append(f'class="{cc}"')
        parts.append('loading="lazy"')
        return '<img ' + ' '.join(parts) + '>'
    c = re.sub(r'<img([^>]*)/?>', img, c)

    # --- enlaces ---
    c = re.sub(r'<a href="([^"]+)"([^>]*)>',
               lambda m: f'<a href="{local_link(m.group(1), lang)}"'
                         + ('' if 'kinolab07.co' not in html.unescape(m.group(1))
                            or 'lenguajeo.kinolab07' in m.group(1)
                            else '') + f'{m.group(2)}>', c)
    # enlaces externos: abrir en pestaña nueva
    c = re.sub(r'<a href="(https?://(?!kinolab07\.co)[^"]+)"([^>]*)>',
               r'<a href="\1" target="_blank" rel="noopener"\2>', c)

    # --- separadores ---
    c = re.sub(r'<hr class="([^"]*)"\s*/?>',
               lambda m: f'<hr{cls_attr(clean_classes(m.group(1)))}>', c)

    # --- resto de atributos de clase ---
    c = re.sub(r'\sclass="([^"]*)"',
               lambda m: cls_attr(clean_classes(m.group(1))), c)
    # --- ruido de WordPress ---
    c = re.sub(r'\s(decoding|loading)="[^"]*"(?=[^>]*>)', '', c, count=0)
    c = c.replace('<img ', '<IMGTMP ')
    c = re.sub(r'\s(decoding|loading)="[^"]*"', '', c)
    c = c.replace('<IMGTMP ', '<img ')
    # los párrafos vacíos del original hacen de separador vertical: se conservan
    c = re.sub(r'<div>[ \t\r\n]*</div>', '', c)
    c = re.sub(r'\n{3,}', '\n\n', c)
    # entidades numéricas -> caracteres reales (los archivos son UTF-8)
    c = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), c)
    c = c.replace('&#038;', '&amp;')
    c = c.replace('\r\n', '\n').replace('\r', '\n')   # WordPress usa CRLF
    return c.strip() + '\n'

def cls_attr(v):
    return f' class="{v}"' if v else ''

def style_attr(attrs):
    m = re.search(r'style="([^"]*)"', attrs)
    if not m:
        return ''
    s = re.sub(r'aspect-ratio:[^;]*;?', '', m.group(1)).strip()
    return f' style="{s}"' if s else ''

def extra_col(tag):
    out = ''
    if 'is-vertically-aligned-center' in tag: out += ' v-center'
    if 'is-vertically-aligned-top' in tag: out += ' v-top'
    return out

if __name__ == '__main__':
    pages = {p['slug']: p for p in json.load(open(f'{ROOT}/reference/pages.json'))}
    meta = {}
    for slug, page in pages.items():
        if slug not in PAGE_OF_SLUG:
            continue
        lang = LANG_OF_SLUG[slug]
        name = PAGE_OF_SLUG[slug]
        out = convert(page['content']['rendered'], lang)
        path = f'{ROOT}/content/{lang}/{name}.html'
        open(path, 'w').write(out)
        meta.setdefault(lang, {})[name] = html.unescape(page['title']['rendered'])
        print(f'{lang}/{name}.html  ({len(out)} bytes)  <- {slug}')
    json.dump(meta, open(f'{ROOT}/reference/titles.json', 'w'),
              indent=1, ensure_ascii=False)
