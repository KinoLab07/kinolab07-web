# kinolab07.co

Sitio de **Enrico Mandirola / KinoLab07** — cine experimental, fotografía y
arte plástico. En línea en <https://www.kinolab07.co>.

Es un sitio estático: HTML y CSS escritos a mano, sin dependencias y sin
proceso de compilación más allá de un script de Python.

## Cómo trabajar

```bash
python3 build.py                 # regenera las páginas
python3 -m http.server 4707      # y abre http://localhost:4707
```

Solo hace falta Python 3.

### Probarlo sin conexión junto al sitio de Lenguajeo

```bash
./tools/probar-offline.sh
```

Genera el sitio en modo local y levanta los dos servidores. **Antes de
publicar hay que volver a generar sin `--local`**, o el botón "Ir a Lenguajeo"
se queda apuntando a `localhost`.

## Estructura

```
build.py              genera el sitio
src/
  site.json           menús, títulos de página, textos de la interfaz
  template.html       plantilla común
content/
  en/*.html           contenido de cada página en inglés
  es/*.html           contenido de cada página en español
assets/
  css/style.css       la hoja de estilo
  css/fuentes.css     las @font-face de Open Sans
  fonts/              Open Sans (4 archivos woff2)
  js/menu.js          menú hamburguesa y desplegables
  images/             las imágenes
  docs/               PDF enlazados desde el contenido
tools/                utilidades de mantenimiento
```

**Los `.html` de la raíz y de `es/` son generados: no los edites a mano.**
Edita `content/` o `src/` y vuelve a ejecutar `python3 build.py`.

- Para cambiar un texto o una imagen: el archivo correspondiente de `content/`.
- Para cambiar el menú o los títulos: `src/site.json`.
- Para cambiar el diseño: `assets/css/style.css`, con las variables de color
  al principio.

## Idiomas

Bilingüe: inglés en la raíz, español en `es/`. Las dos versiones tienen la
misma estructura y las mismas imágenes a la misma medida; conviene mantenerlo
así al añadir contenido.

## Publicación

GitHub Pages desde la rama `main`, carpeta raíz. El archivo `CNAME` fija el
dominio y los certificados se renuevan solos.
