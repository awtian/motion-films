#!/usr/bin/env bash
# Download the fonts that tools/fetch-fonts.mjs does not cover (Git Bash / Linux / macOS):
#   - the CJK vendor fonts (free for commercial use; their vendor sites block scripted downloads, so they come from
#     npm tarballs and GitHub releases; `npm pack` only downloads, it runs no package scripts)
#   - LXGW Marker Gothic (Google Fonts)
#   - the static cuts used by 03-isometric, 07-liquid and 08-morph, instanced from the variable fonts with fonttools
# Needs: npm, curl, unzip, 7-Zip, gh (GitHub CLI), and .venv with fonttools. Run tools/fetch-fonts.mjs first (Unbounded VF).
#
# Usage: bash tools/fetch-cjk-fonts.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CJK="$ROOT/assets/fonts/cjk"
GF=https://raw.githubusercontent.com/google/fonts/main
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
PY="$ROOT/.venv/Scripts/python"; [ -x "$PY" ] || PY="$ROOT/.venv/bin/python"
cd "$TMP"

npm_pkg() { npm pack -q "$1" >/dev/null && mkdir -p "$2" && tar xzf ./*.tgz -C "$2" && rm ./*.tgz; }

echo "Alibaba PuHuiTi 3.0, Alimama ShuHeiTi, Douyin Sans (npm @fontpkg)"
npm_pkg @fontpkg/alibaba-puhuiti-3-0 ali
npm_pkg @fontpkg/alimama-shu-hei-ti alimama
npm_pkg @fontpkg/douyin-sans douyin
mkdir -p "$CJK"/{alibabapuhuiti3,alimamashuheiti,douyinsans,fusionpixel,harmonyossanssc,lxgwmarkergothic}
for w in 105-Heavy 115-Black 55-Regular 65-Medium 85-Bold; do cp "ali/package/AlibabaPuHuiTi-3-$w.ttf" "$CJK/alibabapuhuiti3/"; done
cp alimama/package/AlimamaShuHeiTi-Bold.ttf "$CJK/alimamashuheiti/"
cp douyin/package/DouyinSansBold.otf "$CJK/douyinsans/DouyinSansBold.ttf"   # CFF outlines; fonts.css loads it as is

echo "HarmonyOS Sans SC (github.com/huawei-fonts/HarmonyOS-Sans)"
curl -sfL -o harmony.zip "https://github.com/huawei-fonts/HarmonyOS-Sans/raw/HEAD/HarmonyOS%20Sans.zip"
unzip -q harmony.zip -d harmony
for w in Black Bold Light Medium Regular; do cp "harmony/HarmonyOS Sans/HarmonyOS_Sans_SC/HarmonyOS_Sans_SC_$w.ttf" "$CJK/harmonyossanssc/"; done

echo "Fusion Pixel 12px proportional (github.com/TakWolf/fusion-pixel-font)"
gh release download -R TakWolf/fusion-pixel-font -p "fusion-pixel-font-12px-proportional-ttf-v*.zip"
unzip -q fusion-pixel-font-12px-proportional-ttf-*.zip -d fusion
cp fusion/fusion-pixel-12px-proportional-zh_hans.ttf "$CJK/fusionpixel/"

echo "Resource Han Rounded CN (github.com/CyanoHao/Resource-Han-Rounded)"
Z="$(command -v 7z || echo "/c/Program Files/7-Zip/7z.exe")"
gh release download -R CyanoHao/Resource-Han-Rounded -p "RHR-CN-*.7z"
mkdir -p "$CJK/resourcehanrounded"
"$Z" e -y -o"$CJK/resourcehanrounded" RHR-CN-*.7z ResourceHanRoundedCN-Bold.ttf ResourceHanRoundedCN-Heavy.ttf >/dev/null

echo "LXGW Marker Gothic (Google Fonts)"
curl -sfL -o "$CJK/lxgwmarkergothic/LXGWMarkerGothic-Regular.ttf" "$GF/ofl/lxgwmarkergothic/LXGWMarkerGothic-Regular.ttf"

echo "Static cuts (fonttools varLib.instancer)"
"$PY" -m pip install -q --only-binary=:all: fonttools
curl -sfL -o fraunces.ttf "$GF/ofl/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf"
curl -sfL -o outfit.ttf "$GF/ofl/outfit/Outfit%5Bwght%5D.ttf"
mkdir -p "$ROOT/demos/03-isometric/assets/fonts" "$ROOT/demos/07-liquid/assets" "$ROOT/demos/08-morph/assets/fonts"
"$PY" -m fontTools.varLib.instancer -q fraunces.ttf opsz=72 wght=900 SOFT=100 WONK=0 -o "$ROOT/demos/07-liquid/assets/Fraunces-Liquid-72-900-Soft.ttf"
"$PY" -m fontTools.varLib.instancer -q outfit.ttf wght=600 -o "$ROOT/demos/08-morph/assets/fonts/Outfit-SemiBold.ttf"
"$PY" -m fontTools.varLib.instancer -q "$ROOT/assets/fonts/latin/unbounded/Unbounded-VF.ttf" wght=800 -o "$ROOT/demos/03-isometric/assets/fonts/Unbounded-800-static.ttf"

echo "Check:"
cd "$ROOT"
missing=0
for p in $(grep -o "url('/[^']*')" assets/fonts/fonts.css | sed "s/url('\/\(.*\)')/\1/" | sort -u) \
  demos/03-isometric/assets/fonts/Unbounded-800-static.ttf demos/07-liquid/assets/Fraunces-Liquid-72-900-Soft.ttf \
  demos/08-morph/assets/fonts/Outfit-SemiBold.ttf demos/10-synthwave/assets/fonts/MrDafoe-Regular.ttf; do
  [ -f "$p" ] || { echo "  MISSING $p"; missing=1; }
done
[ $missing = 0 ] && echo "  all fonts in place"
