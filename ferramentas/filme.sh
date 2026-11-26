#!/usr/bin/env bash
# Monta o vídeo do topo do site a partir dos quadros de ferramentas/filme.js.
# Uso: ferramentas/filme.sh <pasta-dos-quadros> [fps=30]
# Gera site/video/heroi.mp4 (H.264), heroi.webm (VP9), as versões de celular heroi-m.* e o pôster heroi.jpg.
set -euo pipefail
Q=${1:?pasta dos quadros}; FPS=${2:-30}
RAIZ=$(cd "$(dirname "$0")/.." && pwd); OUT="$RAIZ/site/video"; mkdir -p "$OUT"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
X=0.5   # duração da transição (o mesmo meio segundo extra que filme.js grava no fim de cada tomada)
dur(){ echo "scale=4; $(ls "$Q"/t$1_*.png | wc -l)/$FPS" | bc; }
D0=$(dur 0); D1=$(dur 1); D2=$(dur 2)
O1=$(echo "$D0-$X" | bc); O2=$(echo "$D0+$D1-2*$X" | bc); TOT=$(echo "$D0+$D1+$D2-2*$X" | bc); FIM=$(echo "$TOT-0.6" | bc)
# tomadas ligadas por fusão; entra e sai do preto para o laço não ter salto
ffmpeg -y -loglevel error \
  -framerate "$FPS" -i "$Q/t0_%04d.png" -framerate "$FPS" -i "$Q/t1_%04d.png" -framerate "$FPS" -i "$Q/t2_%04d.png" \
  -filter_complex "[0][1]xfade=transition=fade:duration=$X:offset=$O1[a];[a][2]xfade=transition=fade:duration=$X:offset=$O2,fade=t=in:st=0:d=0.6,fade=t=out:st=$FIM:d=0.6,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart -an "$TMP/mestre.mp4"
ffmpeg -y -loglevel error -i "$TMP/mestre.mp4" -vf "scale=1280:-2:flags=lanczos" -c:v libx264 -preset slow -crf 25 -profile:v high -pix_fmt yuv420p -movflags +faststart -an "$OUT/heroi.mp4"
ffmpeg -y -loglevel error -i "$TMP/mestre.mp4" -vf "scale=1280:-2:flags=lanczos" -c:v libvpx-vp9 -b:v 0 -crf 36 -row-mt 1 -deadline good -cpu-used 2 -an "$OUT/heroi.webm"
# versão para celular (854 × 480, cerca de metade do tamanho)
ffmpeg -y -loglevel error -i "$TMP/mestre.mp4" -vf "scale=854:-2:flags=lanczos" -c:v libx264 -preset slow -crf 26 -profile:v high -pix_fmt yuv420p -movflags +faststart -an "$OUT/heroi-m.mp4"
ffmpeg -y -loglevel error -i "$TMP/mestre.mp4" -vf "scale=854:-2:flags=lanczos" -c:v libvpx-vp9 -b:v 0 -crf 38 -row-mt 1 -deadline good -cpu-used 2 -an "$OUT/heroi-m.webm"
# pôster: o último quadro da primeira tomada antes da fusão
ffmpeg -y -loglevel error -ss "$(echo "$O1-0.1" | bc)" -i "$TMP/mestre.mp4" -frames:v 1 -q:v 3 "$OUT/heroi.jpg"
ls -la "$OUT"
