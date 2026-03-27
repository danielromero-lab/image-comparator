import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Image Comparator", layout="wide")

st.markdown("""
<style>
[data-testid="column"]:nth-child(3) > div:first-child {
    background-color: #f0f4f8;
    border-radius: 10px;
    border: 1px solid #d0dae4;
    padding: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Image Comparator")
st.markdown("Upload two images to compare them pixel by pixel.")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Image 1")
        file1 = st.file_uploader("Upload first image", type=["png", "jpg", "jpeg", "webp"], key="img1")
        if file1:
            st.image(Image.open(file1).convert("RGB"), use_container_width=True)

with col2:
    with st.container(border=True):
        st.subheader("Image 2")
        file2 = st.file_uploader("Upload second image", type=["png", "jpg", "jpeg", "webp"], key="img2")
        if file2:
            st.image(Image.open(file2).convert("RGB"), use_container_width=True)

with col3:
    st.subheader("Results")
    compare_btn = st.button("Compare Images", type="primary", disabled=not (file1 and file2))

    if compare_btn:
        img1 = Image.open(file1).convert("RGB")
        img2 = Image.open(file2).convert("RGB")

        if img1.size != img2.size:
            st.warning("Different sizes. Resizing second image to match first.")
            img2 = img2.resize(img1.size, Image.LANCZOS)

        arr1 = np.array(img1, dtype=np.float32)
        arr2 = np.array(img2, dtype=np.float32)

        total_pixels = arr1.shape[0] * arr1.shape[1]
        diff_mask = np.any(arr1 != arr2, axis=2)
        pixel_pct = round(int(np.sum(diff_mask)) / total_pixels * 100, 2)
        intensity_pct = round(np.abs(arr1 - arr2).mean() / 255 * 100, 2)

        diff_img = Image.fromarray(
            np.clip(np.abs(arr1 - arr2) * 3, 0, 255).astype(np.uint8)
        )

        m1, m2 = st.columns(2)
        with m1:
            st.metric(
                "Different Pixels", f"{pixel_pct:.2f}%",
                help="Percentage of pixels with any color difference. 0% = identical, 100% = completely different."
            )
        with m2:
            st.metric(
                "Intensity Diff", f"{intensity_pct:.2f}%",
                help="Average magnitude of color change. Low = subtle shifts, High = dramatic differences."
            )

        st.markdown("**Difference Map**")
        st.caption("Brighter = bigger differences. Black = identical pixels.")
        st.image(diff_img, use_container_width=True)
