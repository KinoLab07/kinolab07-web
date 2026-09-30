# Auditoría de kinolab07.co — 2026-09-30

## Qué es hoy
- WordPress (bloques/Gutenberg), tema **Cele 7.1.2** de Compete Themes, sin plugins de página visibles.
- Layout: barra lateral fija a la izquierda (título "Enrico Mandirola" + "KinoLab07", menú vertical, widget con botón "Ir a Lenguajeo"); contenido a la derecha.
- Tipografía: **Open Sans** (300 / 300i / 600) desde Google Fonts.
- Paleta: fondo `#F0F0F0`, texto `#333333`, secundario `#666666`, bordes `#E6E6E6`, acento de enlaces `#A5D3ED`.
- Ancho máximo del contenedor: `1340px`. Breakpoint principal del sidebar: `56.25em` (900px).
- Font Awesome cargado entero (solo para el icono del menú móvil).
- jQuery + jquery-migrate + wp-emoji cargados (no se usan para nada visible).

## Inventario
- **22 páginas publicadas**, 0 entradas de blog.
  - Inglés (en el menú): NEWS (home), BIOGRAPHY, CV, FILMMAKER, WALKING LANGUAGE, ALÉTHEIA, PHOTOGRAPHY, MEMORIES OF SAN PEDRO, MEMORIES OF SAN PEDRO II, PLASTIC ART, LIGHT MESSAGES.
  - Extra en inglés, fuera del menú: A L'AUBE, LENGUAJEO.
  - **Español, huérfanas (no hay menú ni enlace que lleve a ellas):** NOTICIAS, BIOGRAFÍA, CV, CINEMATOGRAFÍA, FOTOGRAFÍAS, ARTES PLASTICAS, MEMORIAS DEL SAN PEDRO, MEMORIAS DEL SAN PEDRO II, MENSAJES DE LUZ, A L'AUBE.
- **65 imágenes** en `/wp-content/uploads/` (2021/09, 2022/01, 2022/05) → **43 MB** en total.
- **2 vídeos Vimeo** embebidos: `299316151` y `7775521`.
- Subdominio aparte: `lenguajeo.kinolab07.co` (otro sitio, "Lenguajeo").

## Problemas encontrados
1. **6 enlaces rotos en el menú FILMMAKER** — devuelven 404: EURITMIA, THE STORY, AT DAWN, MONICA, SIPAR, GAME (`?page_id=` 482, 461, 525, 719, 420, 193). Las páginas se borraron pero siguen en el menú.
2. **Todo el contenido en español es inalcanzable.** Existe una versión ES casi completa sin selector de idioma ni enlaces.
3. **Menú con `?page_id=`** en vez de slugs → enlaces frágiles.
4. **Imágenes sin optimizar**: varias superan 1 MB (la mayor, `Captura-de-pantalla-2022-01-19...png`). Ninguna en formatos modernos salvo un `.webp` suelto.
5. **Carga innecesaria**: Font Awesome completo, jQuery, jQuery Migrate y wp-emoji para una web estática.
6. **URLs de imagen con caracteres no ASCII** (`–`, `â`, `ó`) — dan guerra en Git y en algunos servidores.
7. La home mezcla dos noticias de 2021 sin fecha visible.

## Material descargado en este repo
- `reference/html/*.html` — las 22 páginas renderizadas, tal como las sirve WordPress.
- `reference/assets/css/cele-style.css` — el CSS del tema (45 KB).
- `reference/assets/production.min.js` — el JS del tema.
- `reference/assets/images/` — las 65 imágenes originales (43 MB).
- `reference/pages.json` — volcado de la REST API con el contenido de cada página.
