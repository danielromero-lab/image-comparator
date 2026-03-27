#!/usr/bin/env python3
"""
Image Comparator - Pixel-by-pixel image difference analyzer
Usage: python compare.py image1.png image2.png
"""

import sys
import os
from PIL import Image, ImageChops
import numpy as np


def save_diff_image(path1: str, path2: str, img1: Image.Image, img2: Image.Image):
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    # Absolute difference amplified for visibility
    diff = np.abs(arr1 - arr2)
    diff_amplified = np.clip(diff * 3, 0, 255).astype(np.uint8)
    diff_img = Image.fromarray(diff_amplified)

    base = os.path.splitext(os.path.basename(path1))[0]
    out_path = os.path.join(os.path.dirname(path1), f"{base}_diff.png")
    diff_img.save(out_path)
    return out_path


def compare_images(path1: str, path2: str, save_diff: bool = False) -> dict:
    img1 = Image.open(path1).convert("RGB")
    img2 = Image.open(path2).convert("RGB")

    # Resize img2 to match img1 if sizes differ
    if img1.size != img2.size:
        print(f"Warning: images have different sizes ({img1.size} vs {img2.size}). Resizing second image to match first.")
        img2 = img2.resize(img1.size, Image.LANCZOS)

    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    total_pixels = arr1.shape[0] * arr1.shape[1]

    # Pixels where any channel differs
    diff_mask = np.any(arr1 != arr2, axis=2)
    different_pixels = int(np.sum(diff_mask))
    pixel_difference_pct = (different_pixels / total_pixels) * 100

    # Mean absolute difference per channel (0-255 scale)
    channel_diff = np.abs(arr1 - arr2).mean()
    intensity_difference_pct = (channel_diff / 255) * 100

    diff_path = save_diff_image(path1, path2, img1, img2) if save_diff else None

    return {
        "image1": path1,
        "image2": path2,
        "size": img1.size,
        "total_pixels": total_pixels,
        "different_pixels": different_pixels,
        "pixel_difference_pct": round(pixel_difference_pct, 2),
        "intensity_difference_pct": round(intensity_difference_pct, 2),
        "diff_image": diff_path,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare.py <image1> <image2>")
        sys.exit(1)

    result = compare_images(sys.argv[1], sys.argv[2], save_diff=True)

    print(f"\nImage Comparison Report")
    print(f"{'─' * 40}")
    print(f"Image 1      : {result['image1']}")
    print(f"Image 2      : {result['image2']}")
    print(f"Size         : {result['size'][0]}x{result['size'][1]} px")
    print(f"Total pixels : {result['total_pixels']:,}")
    print(f"{'─' * 40}")
    print(f"Different pixels : {result['different_pixels']:,} ({result['pixel_difference_pct']}%)")
    print(f"Intensity diff   : {result['intensity_difference_pct']}%")
    print(f"{'─' * 40}")
    print(f"Diff image saved : {result['diff_image']}\n")


if __name__ == "__main__":
    main()
