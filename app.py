import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Image Comparator", layout="wide")

st.title("Image Comparator")
st.markdown("Upload two images to compare them pixel by pixel.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Image 1")
    file1 = st.file_uploader("Upload first image", type=["png", "jpg", "jpeg", "webp"], key="img1")
    if file1:
        img1 = Image.open(file1).convert("RGB")
        st.image(img1, use_container_width=True)

with col2:
    st.subheader("Image 2")
    file2 = st.file_uploader("Upload second image", type=["png", "jpg", "jpeg", "webp"], key="img2")
    if file2:
        img2 = Image.open(file2).convert("RGB")
        st.image(img2, use_container_width=True)

with col3:
    st.subheader("Results")
    compare_btn = st.button("Compare Images", type="primary", disabled=not (file1 and file2))

    if compare_btn:
        img1 = Image.open(file1).convert("RGB")
        img2 = Image.open(file2).convert("RGB")

        if img1.size != img2.size:
            st.warning(f"Different sizes ({img1.size} vs {img2.size}). Resizing second image.")
            img2 = img2.resize(img1.size, Image.LANCZOS)

        arr1 = np.array(img1, dtype=np.float32)
        arr2 = np.array(img2, dtype=np.float32)

        total_pixels = arr1.shape[0] * arr1.shape[1]
        diff_mask = np.any(arr1 != arr2, axis=2)
        different_pixels = int(np.sum(diff_mask))
        pixel_pct = round((different_pixels / total_pixels) * 100, 2)

        channel_diff = np.abs(arr1 - arr2).mean()
        intensity_pct = round((channel_diff / 255) * 100, 2)

        diff = np.abs(arr1 - arr2)
        diff_amplified = np.clip(diff * 3, 0, 255).astype(np.uint8)
        diff_img = Image.fromarray(diff_amplified)

        st.metric(label="Different Pixels", value=f"{pixel_pct}%")
        st.caption(
            "Percentage of pixels that have **any** color difference. "
            "0% = identical, 100% = every pixel differs."
        )

        st.metric(label="Intensity Difference", value=f"{intensity_pct}%")
        st.caption(
            "Average **magnitude** of color change. "
            "Low % = subtle shifts. High % = dramatic differences."
        )

        st.markdown("**Difference Map**")
        st.caption("Brighter = bigger differences. Black = identical pixels.")
        st.image(diff_img, use_container_width=True)
