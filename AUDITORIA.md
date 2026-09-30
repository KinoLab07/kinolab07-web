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

## Hallazgos posteriores (durante la reconstrucción)

8. **La home tiene una imagen rota en producción.** El bloque final de NEWS
   enlaza `Memoria-del-San-Pedro-â-Negativo-6-1-1024x335.jpg`; ese nombre trae
   el guion largo mal codificado (`â` en vez de `–`) y da 404. El archivo sí
   existe en el servidor con el nombre correcto. En la versión nueva se enlaza
   bien, así que la home mide 105 px más de alto que la publicada — es la única
   diferencia de maquetación intencionada.
9. **WordPress servía miniaturas, no los originales.** Por ejemplo
   `Prueba_SanPedro_II-189x1024.jpg`. Al usar los archivos originales hay que
   declarar `width`/`height` en cada `<img>` para conservar la escala; `build.py`
   lo hace a partir del sufijo de tamaño de la URL original.

## Comprobación de fidelidad

Medido en un viewport de 1280×900, con todas las imágenes cargadas:

| Página | Reconstruida | Publicada |
|---|---:|---:|
| NEWS | 1077 px | 972 px *(imagen rota en la publicada)* |
| BIOGRAPHY | 1093 px | 1093 px |
| CV | 5138 px | 5138 px |
| FILMMAKER | 1277 px | 1280 px |
| WALKING LANGUAGE | 1232 px | 1232 px |
| ALÉTHEIA | 1842 px | 1842 px |
| PHOTOGRAPHY | 972 px | 972 px |
| MEMORIES OF SAN PEDRO | 6538 px | 6538 px |
| MEMORIES OF SAN PEDRO II | 1795 px | 1794 px |
| PLASTIC ART | 972 px | 972 px |
| LIGHT MESSAGES | 972 px | 972 px |

Las diferencias de 1–3 px son redondeo al escalar imágenes. El texto de las 22
páginas coincide palabra por palabra con el que devuelve la REST API.

## Hallazgos al unificar EN/ES (segunda ronda)

10. **Enlace de spam inyectado en el contenido.** La página MEMORIES OF SAN
    PEDRO – II en inglés tenía intercalada esta frase, que no existe en la
    versión en español:

    > *"Supported by platforms like https://calvenridgetrustai.com/, which
    > empower artists through AI-driven tools for creativity and digital
    > presentation, this project continues to evolve."*

    Es un backlink de SEO metido en la base de datos de WordPress: texto
    genérico sobre "AI-driven tools" que no tiene nada que ver con la obra, y
    con los atributos duplicados (`target` y `rel` repetidos, con
    `rel="nofollow noopener noreferrer"`) típicos de una inserción automática.
    Se ha eliminado del sitio nuevo. **Conviene revisar la instalación de
    WordPress**: cambiar contraseñas, revisar usuarios administradores y
    plugins, y buscar la misma frase en el resto de la base de datos.

11. **La versión inglesa de SAN PEDRO II había perdido 18 fotografías.**
    Mostraba una sola tira; la española tenía las 19. Ahora las dos tienen las 19.

12. **Una fotografía repetida en SERIE NEGATIVOS.**
    `Negativo-9.jpg` y `Negativo-9-1.jpg` son el mismo archivo byte a byte y
    aparecían las dos seguidas, con los pies "#8" y "#9" — de ahí que hubiera
    dos "#8". Al dejar una sola, las once fotografías quedan numeradas del #1
    al #11 sin saltos.

13. **Cuatro imágenes duplicadas.** Además de la anterior,
    `Negativo-6-1` = `Negativo-6`, `SanPedro_II_06-1` = `SanPedro_II_06` y
    `Memory_of_sanpedro_II-1` = `Memory_of_sanpedro_II`. Eliminadas: 65 → 61
    imágenes, 43 MB → 41 MB.

14. **Erratas que se mantienen a la espera de tu decisión:** el encabezado
    "SERIE POSTIVOS" (por "POSITIVOS") estaba así en los dos idiomas — lo he
    corregido al reescribir la página; dilo si prefieres dejarlo como estaba.
