#!/usr/bin/env python3
"""news-image-20261121: THE WORLD TODAY, Saturday 21 November 2026.

Draws a one-page newspaper front page summing up the world's news of
Saturday 21 November 2026, entirely from code: a hand-written 5x7 bitmap
font, a pure-stdlib PNG encoder, and flat vector-style drawing.

Standard library only. No network, no files read, no randomness, no clock:
running it twice writes byte-identical PNGs.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Writes <output>/entry.png (1024x1024, under 1 MiB).
"""

import binascii
import math
import os
import struct
import sys
import zlib

W, H = 1024, 1024

PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (176, 32, 32)
BLUE = (31, 78, 121)
SEA = (174, 205, 226)
LAND = (232, 214, 178)
DARK = (38, 52, 74)
GOLD = (212, 175, 55)
GREEN = (46, 125, 50)
WHITE = (255, 255, 255)
GREY = (120, 116, 104)
LIGHT_BLUE = (210, 226, 240)

# ---------------------------------------------------------------- font ----
# Hand-written 5x7 bitmap font. '#' = ink, '.' = blank. Uppercase, digits
# and the punctuation this page needs.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    # bullet: a small centred block, used as a separator in kickers.
    "\u2022": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}


def text_width(text, scale):
    """Pixel width of text at the given scale (no trailing advance)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def wrap_text(text, scale, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if text_width(trial, scale) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# -------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def put(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.fill_rect(x, y, w, t, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        while True:
            self.fill_rect(x - t // 2, y - t // 2, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def polyline(self, points, color, t=1):
        for a, b in zip(points, points[1:]):
            self.line(a[0], a[1], b[0], b[1], color, t)

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            half = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - half, cy + dy, half * 2 + 1, 1, color)

    def circle(self, cx, cy, r, color, t=2):
        for a in range(0, 360, 2):
            rad = math.radians(a)
            self.fill_rect(int(cx + r * math.cos(rad)) - t // 2,
                           int(cy + r * math.sin(rad)) - t // 2, t, t, color)

    def fill_poly(self, points, color):
        """Scanline polygon fill (points: list of (x, y))."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                self.fill_rect(int(math.ceil(a)), y,
                               int(math.floor(b)) - int(math.ceil(a)) + 1, 1, color)

    def star4(self, cx, cy, r, color):
        """Four-point compass star (NATO-style)."""
        pts = [(cx, cy - r), (cx + r // 4, cy - r // 4), (cx + r, cy),
               (cx + r // 4, cy + r // 4), (cx, cy + r),
               (cx - r // 4, cy + r // 4), (cx - r, cy),
               (cx - r // 4, cy - r // 4)]
        self.fill_poly(pts, color)

    # -- text -------------------------------------------------------------
    def glyph(self, x, y, ch, scale, color):
        rows = FONT.get(ch.upper(), FONT["?"])
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit == "1":
                    self.fill_rect(x + rx * scale, y + ry * scale,
                                   scale, scale, color)

    def text(self, x, y, s, scale, color):
        for ch in s:
            self.glyph(x, y, ch, scale, color)
            x += 6 * scale

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def panel(self, x, y, w, h):
        self.fill_rect(x, y, w, h, WHITE)
        self.rect(x, y, w, h, INK, 2)


# -------------------------------------------------------------- art -------
def draw_spiral(c, cx, cy, color, t=3):
    """Cyclone spiral: an Archimedean spiral drawn as a polyline."""
    pts = []
    steps = 130
    for i in range(steps + 1):
        ang = i / steps * 4.2 * math.pi
        r = 5 + i / steps * 62
        pts.append((int(cx + r * math.cos(ang)),
                    int(cy + r * math.sin(ang) * 0.92)))
    c.polyline(pts, color, t)
    c.fill_circle(cx, cy, 7, color)


def draw_union_jack(c, x, y, w, h):
    c.fill_rect(x, y, w, h, (20, 40, 90))
    c.line(x, y, x + w, y + h, WHITE, 5)
    c.line(x + w, y, x, y + h, WHITE, 5)
    c.line(x, y, x + w, y + h, RED, 2)
    c.line(x + w, y, x, y + h, RED, 2)
    c.fill_rect(x + w // 2 - 6, y, 12, h, WHITE)
    c.fill_rect(x, y + h // 2 - 6, w, 12, WHITE)
    c.fill_rect(x + w // 2 - 3, y, 6, h, RED)
    c.fill_rect(x, y + h // 2 - 3, w, 6, RED)


def draw_eu_flag(c, x, y, w, h):
    c.fill_rect(x, y, w, h, (0, 51, 153))
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 10
    for i in range(12):
        a = math.radians(i * 30 - 90)
        c.fill_circle(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)),
                      4, GOLD)


def draw_globe(c, cx, cy, r):
    c.fill_circle(cx, cy, r, SEA)
    c.circle(cx, cy, r, INK, 3)
    # stylised landmasses
    c.fill_poly([(cx - 52, cy - 18), (cx - 20, cy - 42), (cx + 6, cy - 30),
                 (cx - 4, cy - 6), (cx - 34, cy + 2)], GREEN)
    c.fill_poly([(cx + 12, cy + 8), (cx + 44, cy - 2), (cx + 52, cy + 26),
                 (cx + 22, cy + 40), (cx + 6, cy + 28)], GREEN)
    c.fill_poly([(cx - 40, cy + 26), (cx - 8, cy + 22), (cx - 14, cy + 48),
                 (cx - 44, cy + 44)], GREEN)
    # latitude lines
    for dy, half in ((-r // 2, 0.86), (0, 1.0), (r // 2, 0.86)):
        c.hline(int(cx - r * half), cy + dy, int(2 * r * half), WHITE, 2)
    # sun, clear of the headline: to the right of the globe, mid-height
    sx, sy = cx + r + 32, cy - 6
    c.fill_circle(sx, sy, 16, GOLD)
    for i in range(8):
        a = math.radians(i * 45)
        c.line(int(sx + 20 * math.cos(a)), int(sy + 20 * math.sin(a)),
               int(sx + 30 * math.cos(a)), int(sy + 30 * math.sin(a)), GOLD, 3)


# -------------------------------------------------------------- page ------
def draw_page():
    c = Canvas(W, H, PAPER)
    c.rect(8, 8, W - 16, H - 16, INK, 4)

    # ---- masthead ----
    c.text_center(512, 30, "THE WORLD TODAY", 7, INK)
    c.hline(48, 96, 928, INK, 3)
    c.text_center(512, 106, "SATURDAY 21 NOVEMBER 2026", 3, RED)
    c.text_center(512, 128, "SIX STORIES FROM FIVE CONTINENTS", 2, INK)
    c.hline(24, 152, 976, INK, 2)
    c.hline(24, 156, 976, INK, 1)

    # ---- lead: cyclone Akvan ----
    c.panel(24, 168, 506, 336)
    c.text(40, 182, "INDIA \u2022 CYCLONE AFTERMATH", 2, RED)
    c.text(40, 208, "AKVAN WEAKENS", 4, INK)
    c.text(40, 240, "OVER ODISHA", 4, INK)
    # map art: Bay of Bengal, coast, spiral
    c.fill_rect(40, 282, 474, 150, SEA)
    c.fill_poly([(40, 282), (150, 282), (210, 330), (170, 380), (120, 432),
                 (40, 432)], LAND)
    c.fill_poly([(40, 432), (120, 432), (170, 380), (210, 330), (250, 360),
                 (230, 432)], (196, 178, 138))
    draw_spiral(c, 360, 356, WHITE, 3)
    c.fill_circle(196, 352, 6, RED)
    c.circle(196, 352, 10, RED, 2)
    c.text(212, 344, "GOPALPUR", 2, INK)
    c.text(40, 288, "BAY OF", 2, BLUE)
    c.text(40, 306, "BENGAL", 2, BLUE)
    c.text(40, 448, "440,000 MOVED TO SAFETY AS THE", 2, INK)
    c.text(40, 470, "STORM FADES - NO MAJOR DAMAGE", 2, INK)

    # ---- Poland / NATO ----
    c.panel(546, 168, 454, 156)
    c.text(562, 182, "EUROPE \u2022 NATO ON ALERT", 2, RED)
    c.text(562, 206, "MISSILES IN POLAND", 3, INK)
    c.fill_rect(562, 244, 300, 62, DARK)
    # stylised Poland
    c.fill_poly([(580, 292), (600, 252), (650, 248), (700, 258), (720, 280),
                 (700, 300), (650, 302), (610, 300)], (200, 205, 212))
    for dx, dy in ((640, 272), (672, 288), (700, 268)):
        c.fill_circle(dx, dy, 5, RED)
        c.circle(dx, dy, 8, WHITE, 1)
    c.star4(838, 275, 18, GOLD)
    c.text(562, 312 - 4, "A DAY AFTER THE STRIKES", 2, INK)
    # caption sits just under the art; panel bottom is 324
    # (headline row moved up to fit)

    # ---- Wall Street ----
    c.panel(546, 340, 454, 164)
    c.text(562, 354, "ECONOMY \u2022 WALL STREET", 2, RED)
    c.text(562, 378, "WALL ST SLUMPS", 3, INK)
    c.text(562, 404, "S&P 500 INTO CORRECTION", 2, INK)
    # falling chart
    c.fill_rect(562, 428, 422, 58, LIGHT_BLUE)
    c.line(562, 428, 562, 486, INK, 2)
    c.line(562, 486, 984, 486, INK, 2)
    pts = [(570, 436), (640, 442), (700, 438), (770, 458), (840, 452),
           (910, 472), (972, 480)]
    c.polyline(pts, RED, 3)
    for px, py in pts:
        c.fill_circle(px, py, 3, RED)
    c.text(900, 432, "-3.7%", 2, RED)
    c.text(576, 466, "FRIDAY", 2, BLUE)

    # ---- bottom row ----
    # UK + EU
    c.panel(24, 520, 310, 348)
    c.text(40, 534, "BRITAIN \u2022 EUROPE", 2, RED)
    c.text(40, 558, "UK AND EU SIGN", 3, INK)
    c.text(40, 584, "THREE DEALS", 3, INK)
    draw_union_jack(c, 40, 626, 120, 72)
    draw_eu_flag(c, 178, 626, 120, 72)
    c.text(40, 716, "FOOD, CARBON AND", 2, INK)
    c.text(40, 738, "YOUTH MOBILITY -", 2, INK)
    c.text(40, 760, "SIGNED IN", 2, INK)
    c.text(40, 782, "BRUSSELS", 2, INK)
    c.text(40, 812, "DEALS TO EASE TRADE", 2, GREY)
    c.text(40, 834, "AND TRAVEL", 2, GREY)

    # cricket
    c.panel(357, 520, 310, 348)
    c.text(373, 534, "SPORT \u2022 WELLINGTON", 2, RED)
    c.text(373, 558, "RAHUL'S CENTURY", 3, INK)
    c.text(373, 584, "LIFTS INDIA", 3, INK)
    c.fill_rect(373, 626, 278, 72, DARK)
    c.text_center(512, 640, "IND 344/2", 3, WHITE)
    c.text_center(512, 672, "DAY 3, LUNCH", 2, GOLD)
    # batsman, stumps, ball
    c.fill_rect(373, 716, 278, 84, GREEN)
    c.fill_rect(373, 716, 278, 6, WHITE)
    for sx in (420, 428, 436):
        c.fill_rect(sx, 748, 4, 26, GOLD)
    c.fill_circle(560, 742, 9, INK)          # head
    c.line(560, 751, 556, 786, INK, 5)       # body
    c.line(556, 786, 544, 800, INK, 4)       # legs
    c.line(556, 786, 570, 800, INK, 4)
    c.line(560, 760, 586, 748, INK, 4)       # arms + bat
    c.fill_rect(584, 730, 8, 26, (150, 100, 50))
    c.fill_circle(610, 792, 5, RED)          # ball
    c.text(373, 812, "NZ 368 - NICHOLLS", 2, GREY)
    c.text(373, 834, "175 NOT OUT", 2, GREY)

    # COP31
    c.panel(690, 520, 310, 348)
    c.text(706, 534, "CLIMATE \u2022 TURKEY", 2, RED)
    c.text(706, 558, "CLIMATE TALKS", 3, INK)
    c.text(706, 584, "IN FINAL STAGE", 3, INK)
    draw_globe(c, 800, 676, 58)
    c.text(706, 748, "COP31 NEGOTIATORS", 2, INK)
    c.text(706, 770, "RACE THE CLOCK ON", 2, INK)
    c.text(706, 792, "FOSSIL FUELS AND", 2, INK)
    c.text(706, 814, "CLIMATE FINANCE", 2, INK)
    c.text(706, 834, "IN TURKEY", 2, GREY)

    # ---- footer briefs ----
    c.hline(24, 884, 976, INK, 2)
    c.text(24, 898, "ALSO TODAY: NSE NOW THE WORLD'S 5TH-LARGEST EXCHANGE", 2, INK)
    c.text(24, 922, "HYUNDAI UNVEILS THE 2027 ELANTRA AT THE LOS ANGELES AUTO SHOW", 2, INK)
    c.text_center(512, 950, "ALL THE NEWS OF SATURDAY 21 NOVEMBER 2026 - DRAWN BY CODE", 2, RED)
    c.text_center(512, 980, "THE WORLD TODAY", 2, GREY)
    return c


# -------------------------------------------------------------- png -------
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = draw_page()
    path = os.path.join(out_dir, "entry.png")
    size = write_png(path, canvas)
    print(f"wrote {path} ({canvas.w}x{canvas.h}, {size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
