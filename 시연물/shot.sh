#!/bin/bash
# 헤드리스 크롬으로 화면을 갈무리한다. 검수용.
# 사용법: ./shot.sh <파일명.html> <출력.png> <가로> <세로> [쿼리]
# 프로필을 매번 새로 만들고 시간 제한을 걸어 두어야 크롬이 쌓이지 않는다.
set -u
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FILE="$1"; OUT="$2"; W="${3:-1600}"; H="${4:-900}"; Q="${5:-}"
DIR="$(cd "$(dirname "$0")/.." && pwd)"
URL="file://${DIR}/${FILE}"
[ -n "$Q" ] && URL="${URL}?${Q}"
PROFILE="$(mktemp -d)"
rm -f "$OUT"
( "$CHROME" --headless=new --disable-gpu --no-first-run --no-default-browser-check \
    --user-data-dir="$PROFILE" --hide-scrollbars --force-device-scale-factor=1 \
    --virtual-time-budget=${VT:-1200} --window-size="${W},${H}" \
    --screenshot="$OUT" "$URL" >/dev/null 2>&1 ) &
PID=$!
# 흐름 연출이 켜진 장면은 그래픽 가속 없이 그리느라 오래 걸린다. WAIT로 늘린다.
for _ in $(seq 1 ${WAIT:-70}); do kill -0 "$PID" 2>/dev/null || break; sleep 1; done
kill -9 "$PID" 2>/dev/null
rm -rf "$PROFILE"
[ -f "$OUT" ] && echo "저장 $OUT ($(du -h "$OUT" | cut -f1))" || echo "실패 $OUT"
