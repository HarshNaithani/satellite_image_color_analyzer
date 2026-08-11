import io
from pathlib import Path

import streamlit as st
from PIL import Image

from analyzer import analyze_image, create_chart, create_classified_image
from report import build_report


st.set_page_config(
    page_title="Satellite Image Color Analyzer",
    page_icon="🛰️",
    layout="wide",
)

st.title("🛰️ Satellite Image Color Analyzer")
st.caption(
    "Explainable RGB/HSV prototype for approximate pixel-based land-cover analysis"
)

st.info(
    "Important: this prototype works on image color information. "
    "It reports pixel counts and percentages, not geographic area in m²/hectares. "
    "True NDVI/NDWI/NDBI requires the appropriate multispectral bands."
)

uploaded = st.file_uploader(
    "Upload a satellite image",
    type=["jpg", "jpeg", "png", "webp", "tif", "tiff"],
)

if uploaded is not None:
    try:
        image = Image.open(uploaded).convert("RGB")
    except Exception as exc:
        st.error(f"Could not read the image: {exc}")
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    with st.expander("Image information"):
        st.write(f"Original size: **{image.width} × {image.height} pixels**")
        st.write(f"Total pixels: **{image.width * image.height:,}**")
        st.write(f"Format: **{uploaded.name.split('.')[-1].upper()}**")

    if st.button("🔎 Analyze Image", type="primary"):
        with st.spinner("Analyzing pixels..."):
            result = analyze_image(image)
            classified = create_classified_image(result["labels"])
            chart = create_chart(result["percentages"])

            st.session_state["result"] = result
            st.session_state["classified"] = classified
            st.session_state["chart"] = chart
            st.session_state["image"] = image
            st.session_state["filename"] = uploaded.name

if "result" in st.session_state:
    result = st.session_state["result"]
    classified = st.session_state["classified"]
    chart = st.session_state["chart"]
    image = st.session_state["image"]
    filename = st.session_state["filename"]

    st.divider()
    st.subheader("📊 Analysis Summary")

    categories = ["Vegetation", "Water", "Urban/Built-up", "Other/Land"]
    cols = st.columns(4)

    for col, category in zip(cols, categories):
        with col:
            st.metric(
                category,
                f"{result['percentages'][category]:.2f}%",
                f"{result['counts'][category]:,} pixels",
            )

    left, right = st.columns(2)
    with left:
        st.subheader("Classified Image")
        st.image(classified, use_container_width=True)
    with right:
        st.subheader("Category Distribution")
        st.image(chart, use_container_width=True)

    st.caption(
        "Interpretation: percentages describe the proportion of image pixels "
        "assigned to each class by the RGB/HSV rule-based prototype."
    )

    report_bytes = build_report(
        original=image,
        classified=classified,
        chart=chart,
        result=result,
        source_name=filename,
    )

    classified_buffer = io.BytesIO()
    classified.save(classified_buffer, format="PNG")
    classified_buffer.seek(0)

    st.subheader("💾 Download Outputs")
    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "Download Classified Image",
            data=classified_buffer.getvalue(),
            file_name="classified_image.png",
            mime="image/png",
        )

    with c2:
        st.download_button(
            "Download PDF Report",
            data=report_bytes,
            file_name="satellite_analysis_report.pdf",
            mime="application/pdf",
        )
