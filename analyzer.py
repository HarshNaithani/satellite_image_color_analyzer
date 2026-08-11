from __future__ import annotations

from io import BytesIO
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import rgb_to_hsv


CATEGORIES = ["Vegetation", "Water", "Urban/Built-up", "Other/Land"]

# The prototype uses normalized RGB values [0, 1] and HSV values [0, 1].
# These thresholds are deliberately simple and explainable. They are NOT
# a scientifically validated remote-sensing classifier.
DEFAULT_MAX_SIZE = 1200


def preprocess_image(image: Image.Image, max_size: int = DEFAULT_MAX_SIZE) -> Image.Image:
    """Convert an image to RGB and resize it while preserving aspect ratio."""
    image = image.convert("RGB").copy()
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image


def _classify_pixels(rgb: np.ndarray) -> np.ndarray:
    """
    Classify pixels using transparent RGB/HSV rules.

    Returns an integer label image:
      0 = Vegetation
      1 = Water
      2 = Urban/Built-up
      3 = Other/Land

    This is a baseline prototype. It should not be presented as a validated
    land-cover mapping algorithm.
    """
    x = rgb.astype(np.float32) / 255.0
    hsv = rgb_to_hsv(x)

    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    # Vegetation: green-dominant pixels with sufficient saturation.
    vegetation = (
        (g > r * 1.08)
        & (g > b * 1.05)
        & (g > 0.18)
        & (s > 0.18)
    )

    # Water: blue/cyan-dominant pixels with moderate-to-high saturation
    # and generally lower brightness than bright built-up surfaces.
    water = (
        (b >= r * 1.05)
        & (b >= g * 1.00)
        & (s > 0.18)
        & (v < 0.85)
    )

    # Urban/built-up: relatively neutral, low-saturation surfaces.
    # Very dark neutral pixels are kept as Other/Land to reduce the chance
    # of classifying shadows as built-up.
    urban = (
        (s < 0.22)
        & (v > 0.20)
        & (v < 0.95)
    )

    labels = np.full(r.shape, 3, dtype=np.uint8)
    labels[vegetation] = 0

    # Water gets priority only where vegetation was not selected.
    water_only = water & ~vegetation
    labels[water_only] = 1

    # Urban gets priority only where vegetation/water were not selected.
    urban_only = urban & ~vegetation & ~water
    labels[urban_only] = 2

    return labels


def analyze_image(image: Image.Image) -> Dict:
    """Preprocess and analyze an image, returning counts and percentages."""
    processed = preprocess_image(image)
    rgb = np.asarray(processed, dtype=np.uint8)
    labels = _classify_pixels(rgb)

    counts_array = np.bincount(labels.ravel(), minlength=4)
    total = int(labels.size)

    counts = {
        category: int(counts_array[i])
        for i, category in enumerate(CATEGORIES)
    }
    percentages = {
        category: (counts[category] / total * 100.0) if total else 0.0
        for category in CATEGORIES
    }

    return {
        "labels": labels,
        "counts": counts,
        "percentages": percentages,
        "total_pixels": total,
        "processed_size": processed.size,
    }


def create_classified_image(labels: np.ndarray) -> Image.Image:
    """Create a simple visual map from class labels."""
    # RGB colors for visualization only:
    # vegetation = green, water = blue, urban = gray, other = brown.
    palette = np.array(
        [
            [34, 139, 34],
            [30, 144, 255],
            [128, 128, 128],
            [181, 140, 99],
        ],
        dtype=np.uint8,
    )
    rgb = palette[labels]
    return Image.fromarray(rgb, mode="RGB")


def create_chart(percentages: Dict[str, float]) -> bytes:
    """Create a category-percentage bar chart and return PNG bytes."""
    names = CATEGORIES
    values = [percentages[name] for name in names]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(names, values)
    ax.set_ylabel("Percentage of image pixels")
    ax.set_title("Pixel-based Land-cover Distribution")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return buffer.getvalue()
