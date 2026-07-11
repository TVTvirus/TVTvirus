#!/usr/bin/env python3
"""Genera dark_mode.svg (estilo neofetch/terminal) a partir de:
   - ascii_art.txt  (arte braille de tu cara; regenerable con gen_ascii.py)
   - CONFIG de abajo (edita libremente los campos)
Corre:  python3 make_profile.py
"""

# ============================ EDITA AQUÍ ============================
NAME   = "TVTvirus"          # sale como  TVTvirus@github
HANDLE = "github"

# Cada fila: ("field", clave, valor)  |  ("blank",)
# Quita/añade filas a gusto. NO hay campo de edad a propósito.
ROWS = [
    ("field", "OS",      "Fedora Linux 44 (KDE)  ·  Windows 10"),
    ("field", "Host",    "Self-hosted homelab"),
    ("field", "Role",    "Minecraft server admin @ MineWave"),
    ("field", "IDE",     "VS Code"),
    ("blank",),
    ("field", "Languages.Programming", "Java, Python, Bash"),
    ("field", "Languages.Real",        "Español, English"),
    ("blank",),
    ("field", "Hobbies.Software", "Minecraft modding (Fabric), Discord bots"),
    ("field", "Hobbies.Music",    "double bass · guitar · piano · songwriting"),
    ("blank",),
    ("field", "Now Playing", "Quién va a cantar - Rubén Rada"),
    ("blank",),
    ("field", "Contact.Discord", "TVTvirus"),
    ("field", "Contact.Email",   "tvtvirus2.0@gmail.com"),
]

# Paletas: se genera un SVG por tema (GitHub elige con prefers-color-scheme)
THEMES = {
    "dark_mode.svg": dict(
        BG="#0d1117", BORDER="#30363d",
        C_ART="#b9c0cc",    # la cara
        C_NAME="#7ee787",   # tu nombre
        C_AT="#8b949e",     # @github y la regla
        C_KEY="#58a6ff",    # las claves (OS:, IDE:, ...)
        C_VAL="#c9d1d9",    # los valores
        C_CURSOR="#7ee787",
    ),
    "light_mode.svg": dict(
        BG="#ffffff", BORDER="#d0d7de",
        C_ART="#3f4750",
        C_NAME="#1a7f37",
        C_AT="#59636e",
        C_KEY="#0969da",
        C_VAL="#1f2328",
        C_CURSOR="#1a7f37",
    ),
}
# ===================================================================

FS_ART = 12.5
LH_ART = FS_ART * 1.2          # braille conserva el aspecto con lh = 2*avance (~1.2em)
CH_ART = FS_ART * 0.602        # avance monoespaciado tipico
FS_TXT, LH_TXT = 13.5, 22.0
PAD = 24


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    art = open("ascii_art.txt").read().split("\n")
    art_w = max(len(l) for l in art)
    col2_x = PAD + art_w * CH_ART + 40
    width = int(col2_x + 510)
    height = int(max(len(art) * LH_ART, len(ROWS) * LH_TXT) + PAD * 2 + 16)

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Consolas, \'DejaVu Sans Mono\', '
        f'\'Adwaita Mono\', \'Courier New\', monospace">'
    )
    # Animaciones con fill-mode backwards: por defecto TODO es visible (opacity 1),
    # asi el SVG se ve entero en visores sin CSS; en navegador la animacion
    # aplica el estado from{opacity:0} durante el delay y hace el tipeo.
    out.append(
        "<style>"
        "@keyframes fade{from{opacity:0}to{opacity:1}}"
        "@keyframes blink{50%{opacity:0}}"
        ".art tspan{animation:fade .01s ease backwards}"
        ".row{animation:fade .12s ease backwards}"
        "</style>"
    )
    # marco
    out.append(
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>'
    )

    # ---- arte braille (columna izquierda) ----
    out.append(f'<text class="art" x="{PAD}" y="{PAD+FS_ART}" xml:space="preserve" '
               f'font-size="{FS_ART}" fill="{C_ART}">')
    for i, line in enumerate(art):
        dy = 0 if i == 0 else LH_ART
        out.append(f'<tspan x="{PAD}" dy="{dy}" style="animation-delay:{0.02*i:.2f}s">{esc(line)}</tspan>')
    out.append("</text>")

    # ---- campos (columna derecha) ----
    y = PAD + FS_TXT
    art_done = 0.02 * len(art)
    line_idx = 0

    def row_text(inner, delay):
        return (f'<text class="row" x="{col2_x}" y="{y}" font-size="{FS_TXT}" '
                f'xml:space="preserve" style="animation-delay:{delay:.2f}s">{inner}</text>')

    # titulo:  NAME@github  +  regla
    inner = (f'<tspan fill="{C_NAME}" font-weight="bold">{esc(NAME)}</tspan>'
             f'<tspan fill="{C_AT}">@{esc(HANDLE)}</tspan>')
    out.append(row_text(inner, art_done + 0.10)); y += LH_TXT; line_idx += 1
    rule = "-" * (len(NAME) + 1 + len(HANDLE))
    out.append(row_text(f'<tspan fill="{C_AT}">{rule}</tspan>', art_done + 0.22)); y += LH_TXT; line_idx += 1

    for row in ROWS:
        d = art_done + 0.10 + 0.12 * line_idx
        if row[0] == "blank":
            y += LH_TXT * 0.5; line_idx += 1; continue
        _, key, val = row
        inner = (f'<tspan fill="{C_KEY}" font-weight="bold">{esc(key)}</tspan>'
                 f'<tspan fill="{C_AT}">: </tspan>'
                 f'<tspan fill="{C_VAL}">{esc(val)}</tspan>')
        out.append(row_text(inner, d)); y += LH_TXT; line_idx += 1

    # cursor: aparece al final y parpadea (visible fijo en visores sin CSS)
    d = art_done + 0.10 + 0.12 * line_idx
    out.append(f'<text x="{col2_x}" y="{y}" font-size="{FS_TXT}" fill="{C_CURSOR}" '
               f'style="animation:fade .01s backwards {d:.2f}s, blink 1.1s steps(1) {d+.3:.2f}s infinite">'
               f'&#9611;</text>')

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    for fname, theme in THEMES.items():
        globals().update(theme)      # build() lee los colores como globales
        svg = build()
        with open(fname, "w") as f:
            f.write(svg)
        print(f"Escrito {fname} ({len(svg)} bytes)")
