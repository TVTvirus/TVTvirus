#!/usr/bin/env python3
"""Convierte tu imagen de perfil en arte braille (ascii_art.txt).
Braille = 2x4 puntos por caracter, mucha mas resolucion que ASCII clasico.
Ajusta WIDTH o CROP y vuelve a correrlo; luego make_profile.py."""
import numpy as np
from PIL import Image, ImageOps

SRC   = "/mnt/games/Program files/Imagenes/b017c439-c8e8-446b-8abd-56414081d0b6-profile_image-300x300.png"
OUT   = "ascii_art.txt"
WIDTH = 64                    # ancho en caracteres
CROP  = (58, 22, 288, 224)    # (left, top, right, bottom) zoom a la cara; None = entera

img = Image.open(SRC).convert("RGBA")
bg = Image.new("RGBA", img.size, (255, 255, 255, 255))   # aplana alpha sobre blanco
img = Image.alpha_composite(bg, img).convert("L")
if CROP:
    img = img.crop(CROP)
img = ImageOps.autocontrast(img, cutoff=1)

# celda braille = 2x4 puntos -> el aspecto real se conserva con line-height = 2*char
w, h = img.size
px_w = WIDTH * 2
px_h = int(px_w * h / w)
px_h -= px_h % 4
img = img.resize((px_w, px_h))

# dither Floyd-Steinberg: el gris se vuelve textura de puntos, las lineas quedan solidas
dots = ~np.asarray(img.convert("1", dither=Image.FLOYDSTEINBERG))  # True = oscuro

BITS = [(0, 0, 0x01), (1, 0, 0x02), (2, 0, 0x04), (3, 0, 0x40),
        (0, 1, 0x08), (1, 1, 0x10), (2, 1, 0x20), (3, 1, 0x80)]
H, W = dots.shape
lines = []
for cy in range(0, H, 4):
    line = []
    for cx in range(0, W, 2):
        code = 0x2800                       # U+2800 en blanco = mantiene el monoespaciado
        for dy, dx, bit in BITS:
            if cy + dy < H and cx + dx < W and dots[cy + dy, cx + dx]:
                code |= bit
        line.append(chr(code))
    lines.append("".join(line))

with open(OUT, "w") as f:
    f.write("\n".join(lines))
print(f"Escrito {OUT}: {len(lines[0])}x{len(lines)} chars (braille)")
