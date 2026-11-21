"""Build the README cover banner: docs/img/banner.png.

Left: |B| of a single current loop, cut through its axis (the xz-plane), with
field lines, computed by pinnfield.biot_savart. Right: the rig concept render.
Title and tagline across the middle.

Run from the repo root:
    python scripts/make_banner.py

Needs matplotlib and pillow on top of the project requirements. Later, swap
`field_panel` for a "PINN prediction vs. measured" plot and rerun.
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.patches import Circle, FancyBboxPatch
from PIL import Image
import logging

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from pinnfield.biot_savart import loop_field  # noqa: E402

OUT = REPO / "docs" / "img" / "banner.png"
RENDER = REPO / "docs" / "img" / "cover-render.png"

BG = "#0b1020"  # page background
INK = "#f3f4f6"  # title text
MUTED = "#9aa4b8"  # tagline text
ACCENT = "#f5a65b"  # copper, matches the coil in the render

WIDTH_IN, HEIGHT_IN, DPI = 12.8, 4.0, 150  # 1920 x 600 px

plt.rcParams["font.family"] = ["Inter", "Helvetica Neue", "Arial", "DejaVu Sans"]


def compute_field(radius_m=0.05, current_a=1.0, nx=320, nz=200):
    """|B| and (Bx, Bz) on a grid in the xz-plane through the loop's axis."""
    x = np.linspace(-2.6 * radius_m, 2.6 * radius_m, nx)
    z = np.linspace(-2.0 * radius_m, 2.0 * radius_m, nz)
    X, Z = np.meshgrid(x, z)
    pts = np.stack([X.ravel(), np.zeros(X.size), Z.ravel()], axis=1)
    B = loop_field(pts, radius_m, current_a, n_segments=400).reshape(nz, nx, 3)
    return x, z, B[..., 0], B[..., 2], np.linalg.norm(B, axis=-1)


def field_panel(ax, radius_m=0.05):
    x, z, bx, bz, mag = compute_field(radius_m)
    # Dark navy -> violet -> copper -> warm white, so the hot spots echo the coil.
    cmap = LinearSegmentedColormap.from_list(
        "copper_field", [BG, "#1d2a5c", "#5b3a8a", "#c0566b", ACCENT, "#fff1d6"]
    )
    vmin, vmax = np.percentile(mag, 2), np.percentile(mag, 99.3)
    ax.imshow(
        np.clip(mag, vmin, vmax),
        extent=(x[0], x[-1], z[0], z[-1]),
        origin="lower",
        cmap=cmap,
        norm=LogNorm(vmin=vmin, vmax=vmax),
        interpolation="bicubic",
        aspect="auto",
    )
    ax.streamplot(
        x, z, bx, bz,
        color=(1, 1, 1, 0.30),
        linewidth=0.6,
        density=0.9,
        arrowstyle="-",
        broken_streamlines=False,
    )
    # The two places the wire pierces the plane: current out of / into the page.
    for sx, mark in ((-radius_m, "•"), (radius_m, "×")):
        ax.add_patch(Circle((sx, 0), radius_m * 0.12, color="#fff1d6", zorder=5))
        ax.text(sx, 0, mark, ha="center", va="center", fontsize=8,
                color=BG, zorder=6, fontweight="bold")
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(z[0], z[-1])
    ax.axis("off")


def fade_right(fig, rect, start=0.55):
    """Fade the right edge of an axes rectangle into the background."""
    ax = fig.add_axes(rect, zorder=2)
    ramp = np.clip((np.linspace(0, 1, 256) - start) / (1 - start), 0, 1)
    rgba = np.zeros((1, 256, 4))
    rgba[..., :3] = matplotlib.colors.to_rgb(BG)
    rgba[..., 3] = ramp**1.4
    ax.imshow(rgba, aspect="auto", extent=(0, 1, 0, 1))
    ax.axis("off")


def render_panel(fig, rect):
    """Crop the rig render and place it in a rounded card."""
    img = Image.open(RENDER).convert("RGB")
    w, h = img.size
    img = img.crop((int(0.03 * w), int(0.12 * h), int(0.98 * w), int(0.92 * h)))
    ax = fig.add_axes(rect, zorder=3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    card = FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0,rounding_size=0.035",
        transform=ax.transAxes, facecolor="#eff0f2", edgecolor="none",
    )
    im = ax.imshow(img, extent=(0, 1, 0, 1), aspect="auto")
    im.set_clip_path(card)  # rounds the image corners


def main():
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI, facecolor=BG)

    field_ax = fig.add_axes((0, 0, 0.36, 1), zorder=1)
    field_panel(field_ax)
    fade_right(fig, (0, 0, 0.36, 1), start=0.45)

    # Render card, sized to the cropped image's aspect ratio.
    card_h = 0.60
    card_w = card_h * (HEIGHT_IN / WIDTH_IN) * (0.95 * 2400) / (0.80 * 1500)
    render_panel(fig, (0.975 - card_w, (1 - card_h) / 2, card_w, card_h))

    tx = 0.305
    fig.text(tx, 0.67, "B-FIELD MAPPING", color=ACCENT, fontsize=11,
             fontweight="bold", ha="left", zorder=4)
    fig.text(tx, 0.53, "pinn-field-mapping", color=INK, fontsize=27,
             fontweight="bold", ha="left", va="center", zorder=4)
    fig.text(tx, 0.37,
             "Sparse magnetic field reconstruction with\n"
             "physics-informed neural networks and active sampling",
             color=MUTED, fontsize=10.5, ha="left", va="center",
             linespacing=1.5, zorder=4)
    fig.text(0.012, 0.04,
             "|B| of a current loop, cut through its axis (Biot–Savart, src/pinnfield)",
             color=(1, 1, 1, 0.45), fontsize=7, ha="left", zorder=4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI, facecolor=BG)
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
