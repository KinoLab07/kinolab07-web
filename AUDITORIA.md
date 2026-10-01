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

## Lo que apareció en el backup de WordPress (1 de octubre de 2026)

El paquete `entrega-enrico` preparado por David Vega resolvió casi todo lo que
quedaba abierto.

15. **Las doce páginas que faltaban no se habían borrado: estaban en borrador.**
    Por eso el menú daba 404 y por eso no salían en la API pública, que solo
    devuelve lo publicado. Están todas en la tabla `DrB_posts`, con fecha de
    modificación del **21 de julio de 2026** — el mismo día en que se neutralizó
    el ataque de spam. Es muy probable que se despublicaran durante aquella
    limpieza y nadie se diera cuenta.

    | ID | Página | Idioma |
    |---|---|---|
    | 193 / 709 | GAME / JUEGO | EN / ES |
    | 420 / 714 | SIPAR | EN / ES |
    | 445 / 719 | MONICA | ES / EN |
    | 461 / 699 | THE STORY / EL CUENTO | EN / ES |
    | 482 / 704 | EURITMIA | EN / ES |
    | 525 / 672 | AT DAWN / A L'AUBE | EN / ES |
    | 527 / 679 | ALÉTHEIA | EN / ES |

    Ojo al detalle de MONICA: la página en español es la 445 y la inglesa la
    719, al revés que en el resto de las parejas.

16. **Existían las versiones del autor de AT DAWN en inglés y ALÉTHEIA en
    español**, que yo había traducido a mano. Las traducciones se han
    sustituido por los textos originales de Enrico.

17. **Las once imágenes que necesitaban esas páginas estaban en el backup.**
    Siete eran nuevas; las otras cuatro resultaron ser duplicados exactos de
    imágenes que ya teníamos. Total: 61 → 68 imágenes.

18. **Había dos menús, y el español nunca se asignó a ninguna posición del
    tema.** Se llamaban "HOME" (español) y "HOME ENGLISH" (inglés, asignado a
    `primary`). Esa es la explicación de por qué todo el contenido en español
    era inalcanzable. La estructura del menú español coincide con la que
    habíamos reconstruido, salvo en un detalle: en FOTOGRAFÍAS el original
    ponía MEMORIAS DEL SAN PEDRO – II **antes** que MEMORIAS DEL SAN PEDRO.
    Aquí van en el mismo orden que en inglés; dilo si prefieres el original.

19. **El enlace de spam sigue vivo en la base de datos.** `calvenridgetrustai.com`
    aparece dos veces en el volcado del 30 de septiembre: en la página 327
    (MEMORIES OF SAN PEDRO – II, publicada) y en una revisión. La limpieza de
    julio se lo dejó. En el sitio nuevo ya no está, pero **sigue publicado en
    el WordPress de hoy**. Conviene avisar a David.

    El resto del spam sí se limpió bien: cero enlaces ocultos con
    `position:absolute`, cero dominios de casino o apuestas, en los dos
    WordPress.

20. **El backup contiene contraseñas, al contrario de lo que dice su propia
    nota.** `LEEME-para-Claude.md` afirma que el volcado va sin las tablas de
    usuarios. Es cierto para las tablas `DrB_*`, pero **no** para `kino_users`,
    `wpqx_users` ni las de clases: ahí hay dos cuentas de administrador con su
    hash de contraseña (`$P$...`), el correo y tokens de sesión con direcciones
    IP. Ver la advertencia del README.

## Unificación EN/ES de fotos y CV (1 de octubre de 2026)

Las dos versiones de cada página mostraban las mismas fotos a tamaños
distintos, y el CV usaba estructuras de maquetación diferentes. Ahora **las 17
parejas coinciden en imágenes y en estructura**, comprobado archivo a archivo.

### El CV

Eran dos maquetaciones distintas del mismo contenido:

- El inglés agrupaba cada sección en un `<p>` con las entradas separadas por
  `<br>`, y metía las listas de festivales en un `<ul>` con viñetas.
- El español ponía **cada línea en su propio `<h6>`**, con `<h6>` vacíos de
  relleno entre secciones y los años subrayados con `<u>`.

De ahí el interlineado distinto: `<p>` tiene margen de 1,5 em entre bloques y
`<h6>` tiene margen cero. El español pasa a la estructura del inglés, y las
tres listas con viñetas del inglés pasan a líneas como en español. Los dos
quedan con **12 bloques, los mismos y con el mismo número de líneas cada uno**.

### Las fotos

Regla aplicada: misma medida en los dos idiomas, proporción real del archivo
(se comprobó que ninguna queda deformada, desvío máximo del 0,5%) y sin
agrandar más de lo que el autor ya hacía.

| Página | Antes (EN / ES) | Ahora |
|---|---|---|
| BIOGRAPHY | 412 ancho / 300×224 | 412×307 |
| EURITMIA | 654×368 / 690 ancho | 601×339 *(tamaño real; las dos agrandaban)* |
| THE STORY | 269 y 271 / 335 y 333 | 269×179 y 271×180 |
| A L'AUBE | 329×247 / 319 ancho | 319×240 |
| GAME | 209×167 / tamaño real | tamaño real |
| LIGHT MESSAGES | 347×230 / 354 ancho | 354×235 |
| PLASTIC ART | 246×163 / 246 con recorte | 246×163 |
| PHOTOGRAPHY | las cuatro forzadas a 309×86 | 309 de ancho, alto proporcional |

En PHOTOGRAPHY el inglés forzaba las cuatro fichas a la misma caja, lo que
**deformaba dos de ellas**: tienen proporción 2,08 y 2,24 y se estiraban a
3,59. Ahora comparten ancho y cada una conserva su alto.

Dos de las imágenes de THE STORY son originales de solo 200 y 203 píxeles de
ancho; en el backup no hay versión mayor, así que a 269 se ven algo blandas.
Si aparecen los originales en mejor resolución, se sustituyen y listo.

### Envolturas sobrantes

Al comparar estructuras aparecieron envoltorios que solo estaban en un idioma:
un `<div>` que rodeaba todo el texto de JUEGO, otro alrededor de la rejilla de
FILMMAKER, divs de maquetación de PDF en BIOGRAFÍA y un `<div>` de más en cada
columna de FOTOGRAFÍAS. Fuera todos.

### Páginas que no existen en ninguna parte

**DESARROLLO ARMÓNICO**, **CHROMATIC FILMIC TERRITORIES / TERRITORIOS FÍLMICOS
CROMÁTICOS** y la **ALÉTHEIA fotográfica** aparecían como fichas con imagen y
pie en las páginas FILMMAKER y PHOTOGRAPHY, pero **no eran enlaces y no existía
ninguna página detrás**, ni publicada ni en borrador, ni en la web ni en el
backup. Nunca se escribieron.

Por decisión de Enrico (1 de octubre de 2026) se han retirado de las dos
páginas y en los dos idiomas, junto con sus tres imágenes. FILMMAKER pasa de
nueve fichas a ocho, repartidas 3+3+2 para que las columnas sigan midiendo un
tercio; PHOTOGRAPHY pasa de cuatro a dos. Las imágenes siguen en el backup
(`armonico.webp`, `Screen-Shot-2021-09-20-at-2.23.46-PM.png` y
`Screen-Shot-2021-09-20-at-2.25.45-PM.png`) por si algún día se escriben.

Al reconstruir FILMMAKER apareció además que la versión inglesa tenía cuatro
`</div>` de más, residuo de haber quitado una envoltura: el navegador lo
toleraba, pero el HTML estaba mal cerrado. Las dos versiones se generan ahora
desde la misma lista de películas, así que no pueden volver a divergir.
