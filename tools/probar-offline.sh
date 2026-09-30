#!/usr/bin/env bash
# Levanta los dos sitios en local y los enlaza entre sí, sin tocar internet.
#
#   ./tools/probar-offline.sh            busca Lenguajeo en ../lenguajeo-web
#   ./tools/probar-offline.sh /otra/ruta
#
# Ctrl+C para parar los dos.
set -euo pipefail

cd "$(dirname "$0")/.."
SITIO=$(pwd)
LENGUAJEO="${1:-$SITIO/../lenguajeo-web}"

echo "Generando el sitio en modo local..."
python3 build.py --local

limpiar() {
  echo
  echo "Parando los servidores..."
  kill $(jobs -p) 2>/dev/null || true
  echo "Recuerda: 'python3 build.py' sin --local antes de publicar."
}
trap limpiar EXIT

python3 -m http.server 4707 --directory "$SITIO" >/dev/null 2>&1 &

if [ -d "$LENGUAJEO" ]; then
  python3 -m http.server 4708 --directory "$LENGUAJEO" >/dev/null 2>&1 &
  echo "  Lenguajeo  ->  http://localhost:4708"
else
  echo "  (no encuentro Lenguajeo en $LENGUAJEO; paso de levantarlo)"
fi

sleep 1
echo "  kinolab07  ->  http://localhost:4707"
echo
echo "Ctrl+C para parar."
wait
