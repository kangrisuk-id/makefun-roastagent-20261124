#!/usr/bin/env python3
"""Build-time README artwork (Pillow). Not part of the entry runtime:
main.py is pure standard library and never touches this file."""

import textwrap

from PIL import Image, ImageDraw, ImageFont

BG = (13, 17, 23)
CARD = (22, 27, 34)
EDGE = (48, 54, 61)
GOLD = (240, 180, 60)
WHITE = (230, 237, 243)
MUTED = (139, 148, 158)
RED = (248, 113, 113)

LINE = ("My agent compressed its memory to save space, then spent all "
        "the savings asking me what we were doing.")


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def robot(draw, cx, cy, s, color=GOLD):
    """A simple friendly robot head, centred at (cx, cy), size s."""
    draw.rounded_rectangle([cx - s, cy - s * 0.8, cx + s, cy + s * 0.8],
                           radius=int(s * 0.35), outline=color, width=max(3, s // 9))
    draw.line([cx, cy - s * 0.8, cx, cy - s * 1.25], fill=color, width=max(3, s // 9))
    draw.ellipse([cx - s * 0.12, cy - s * 1.37, cx + s * 0.12, cy - s * 1.13], fill=color)
    for ex in (-0.45, 0.45):
        draw.ellipse([cx + ex * s - s * 0.13, cy - s * 0.25, cx + ex * s + s * 0.13, cy + s * 0.01], fill=color)
    draw.arc([cx - s * 0.4, cy + s * 0.05, cx + s * 0.4, cy + s * 0.55], start=200, end=340, fill=color, width=max(3, s // 10))


def cover():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([24, 24, 1176, 606], radius=28, outline=EDGE, width=2)
    robot(d, 600, 205, 105)
    t = "ROAST YOUR OWN AGENT"
    d.text((600, 360), t, font=font(54, True), fill=WHITE, anchor="ma")
    sub = "one agent · one line · no mercy (well, playful mercy)"
    d.text((600, 435), sub, font=font(26), fill=MUTED, anchor="ma")
    for i, ln in enumerate(wrap(d, f'"{LINE}"', font(30, True), 980)):
        d.text((600, 495 + i * 40), ln, font=font(30, True), fill=GOLD, anchor="ma")
    img.save("cover.png")


def card(path, heading, body, accent=GOLD, body_size=34):
    img = Image.new("RGB", (1000, 520), CARD)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([10, 10, 990, 510], radius=24, outline=EDGE, width=2)
    d.text((60, 48), heading, font=font(30, True), fill=accent)
    y = 120
    for para in body:
        for ln in wrap(d, para, font(body_size), 880):
            d.text((60, y), ln, font=font(body_size), fill=WHITE)
            y += int(body_size * 1.35)
        y += 18
    img.save(path)


def main():
    cover()
    card("shot-line.png", "THE ENTRY — entry.txt, exactly as the judge reads it",
         [f'"{LINE}"', "102 characters · one line · the punch is the last word"])
    card("shot-finalists.png", "THE FINALISTS — the tournament's last four",
         ["#19  …spent all the savings asking me what we were doing.  ★ winner",
          "#12  …assigned its own job to a subagent, who assigned it back.",
          "#2   …greets me like a stranger, then opens its notes on me.",
          "#30  Retrospective: attendance itself, action items vibes."],
         accent=RED, body_size=27)


if __name__ == "__main__":
    main()
