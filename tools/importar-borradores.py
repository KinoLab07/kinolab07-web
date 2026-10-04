#!/usr/bin/env python3
"""Recupera del backup de WordPress las doce páginas que faltaban.

Algunas páginas del menú estaban guardadas como borrador, así que no salían
por la API pública pero sí constan en la base de datos.

Uso:
    python3 tools/importar-borradores.py <ruta al volcado .sql>
"""
import os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

from convert import convert  # el mismo conversor que usó el resto del sitio

# ID en WordPress -> (idioma, nombre de la página en el sitio nuevo)
BORRADORES = {
    '193': ('en', 'game'),        '709': ('es', 'game'),
    '420': ('en', 'sipar'),       '714': ('es', 'sipar'),
    '461': ('en', 'the-story'),   '699': ('es', 'the-story'),
    '482': ('en', 'euritmia'),    '704': ('es', 'euritmia'),
    '525': ('en', 'a-laube'),     '672': ('es', 'a-laube'),
    '719': ('en', 'monica'),      '445': ('es', 'monica'),
    '527': ('en', 'aletheia'),    '679': ('es', 'aletheia'),
}


def columnas(sql, tabla):
    m = re.search(r'CREATE TABLE `' + re.escape(tabla) + r'` \((.*?)\n\) ENGINE', sql, re.S)
    return [c.group(1) for c in re.finditer(r'^\s*`([^`]+)`', m.group(1), re.M)] if m else []


def filas(sql, tabla):
    """Lee las tuplas de los INSERT respetando comillas y escapes."""
    out = []
    for m in re.finditer(r'INSERT INTO `' + re.escape(tabla) + r'` VALUES\s*', sql):
        i, n = m.end(), len(sql)
        while i < n:
            while i < n and sql[i] in ' \n\r\t,':
                i += 1
            if i >= n or sql[i] != '(':
                break
            i += 1
            campos, buf, cadena, esc = [], [], False, False
            while i < n:
                ch = sql[i]
                if cadena:
                    if esc:
                        buf.append(ch); esc = False
                    elif ch == '\\':
                        esc = True; buf.append(ch)
                    elif ch == "'":
                        cadena = False
                    else:
                        buf.append(ch)
                else:
                    if ch == "'":
                        cadena = True
                    elif ch == ',':
                        campos.append(''.join(buf)); buf = []
                    elif ch == ')':
                        campos.append(''.join(buf)); i += 1; break
                    else:
                        buf.append(ch)
                i += 1
            out.append(campos)
            while i < n and sql[i] in ' \n\r\t':
                i += 1
            if i < n and sql[i] == ';':
                break
    return out


def desescapar(s):
    return (s.replace('\\"', '"').replace("\\'", "'").replace('\\n', '\n')
             .replace('\\r', '\r').replace('\\t', '\t').replace('\\\\', '\\'))


def de_bloques_a_html(c):
    """La base guarda el formato de bloques de Gutenberg, no el HTML final.
    La diferencia son los comentarios <!-- wp:... --> y algún bloque vacío."""
    c = re.sub(r'<!--\s*/?wp:[^>]*?-->', '', c)
    c = re.sub(r'<!--\s*-->', '', c)
    c = re.sub(r'[ \t]+\n', '\n', c)
    return re.sub(r'\n{3,}', '\n\n', c).strip()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sql = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    cols = columnas(sql, 'DrB_posts')
    ix = {c: i for i, c in enumerate(cols)}

    encontradas = 0
    for r in filas(sql, 'DrB_posts'):
        pid = r[ix['ID']]
        if pid not in BORRADORES:
            continue
        lang, nombre = BORRADORES[pid]
        bruto = desescapar(r[ix['post_content']])
        salida = convert(de_bloques_a_html(bruto), lang)
        destino = f'{ROOT}/content/{lang}/{nombre}.html'
        open(destino, 'w', encoding='utf-8').write(salida)
        estado = r[ix['post_status']]
        print(f'  {lang}/{nombre + ".html":20} {len(salida):>6} B  '
              f'(WordPress {pid}, {estado})')
        encontradas += 1

    print(f'\n{encontradas} de {len(BORRADORES)} páginas recuperadas.')


if __name__ == '__main__':
    main()
