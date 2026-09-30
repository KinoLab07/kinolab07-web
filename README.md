# kinolab07.co

Sitio estático de **Enrico Mandirola / KinoLab07**, reconstruido a partir de la web
en WordPress (tema Cele) para poder editarlo sin depender de WordPress.

El resultado es visualmente idéntico al sitio publicado: mismos colores, misma
tipografía (Open Sans 300/600), mismos anchos y los mismos puntos de corte
responsive. Ya no carga jQuery, jQuery Migrate, wp-emoji ni Font Awesome.

## Estructura

```
.
├── build.py              genera el sitio  ->  python3 build.py
├── src/
│   ├── site.json         menús, títulos de página, textos de la interfaz
│   └── template.html     plantilla común de todas las páginas
├── content/
│   ├── en/*.html         contenido de cada página en inglés
│   └── es/*.html         contenido de cada página en español
├── assets/
│   ├── css/style.css     toda la hoja de estilo
│   ├── js/menu.js        menú hamburguesa y desplegables
│   └── images/           65 imágenes
├── reference/            material original de WordPress (solo consulta)
│   ├── html/             las 22 páginas tal como las servía WordPress
│   ├── pages.json        volcado de la REST API
│   └── assets/css/       el CSS del tema Cele
│
├── index.html, *.html    páginas generadas en inglés
└── es/*.html             páginas generadas en español
```

**Los `.html` de la raíz y de `es/` son generados: no los edites a mano.**
Edita `content/` o `src/` y vuelve a ejecutar `python3 build.py`.

## Cómo trabajar

```bash
python3 build.py                 # regenera las 34 páginas
python3 -m http.server 4707      # y abre http://localhost:4707
```

No hace falta instalar nada: solo Python 3.

### Cambiar el texto o las imágenes de una página
Edita el fragmento correspondiente en `content/en/` o `content/es/` y reconstruye.
Las rutas de imagen dentro de los fragmentos se escriben siempre como
`assets/images/...`; `build.py` les añade el `../` cuando toca.

### Cambiar el menú o los títulos
Todo está en `src/site.json`.

### Cambiar el diseño
Todo está en `assets/css/style.css`, organizado por secciones y con las variables
de color al principio.

## Idiomas

El sitio es bilingüe: inglés en la raíz, español en `es/`. En WordPress las
páginas en español existían pero no eran accesibles desde ningún menú; aquí
tienen su propio menú y un selector EN/ES en la barra lateral.

## Páginas pendientes de contenido

Estas doce páginas están en el menú pero todavía no tienen contenido (en
WordPress los enlaces daban 404 porque las páginas se habían borrado). Muestran
un aviso de "en construcción" hasta que se rellenen: crea el fragmento
`content/en/<pagina>.html` o `content/es/<pagina>.html` y reconstruye.

| Página | Inglés | Español |
|---|---|---|
| EURITMIA        | falta | falta |
| THE STORY / EL CUENTO | falta | falta |
| MONICA          | falta | falta |
| SIPAR           | falta | falta |
| GAME / JUEGO    | falta | falta |
| AT DAWN / A L'AUBE | falta | **ya existe** |
| ALÉTHEIA        | **ya existe** | falta |

## Publicar en GitHub Pages

El repositorio ya está listo: incluye `.nojekyll` y las páginas se sirven desde
la raíz.

1. Crea el repositorio en GitHub y súbelo.
2. En *Settings → Pages*, elige *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
3. Para usar el dominio propio, añade un archivo `CNAME` con `www.kinolab07.co`
   y apunta el DNS a GitHub Pages.

## Herramientas

`tools/convert.py` fue el conversor de un solo uso que tradujo el HTML de bloques
de WordPress (`reference/pages.json`) a los fragmentos limpios de `content/`.
Se conserva para poder repetir la importación si hiciera falta.
