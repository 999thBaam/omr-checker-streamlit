import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
import tempfile
import fitz  # PyMuPDF

# Title
st.title("📝 OMR Sheet Checker App")
st.write("Upload a scanned OMR sheet and compare it with the answer key to get the score.")

# Upload answer key
key_file = st.file_uploader("Upload Answer Key (Excel)", type=["xlsx"])
if key_file:
    key_df = pd.read_excel(key_file)
    answer_key = key_df['Answer'].tolist()
    st.success("✅ Answer key loaded")

# Upload OMR image or PDF
uploaded_file = st.file_uploader("Upload OMR Sheet (Image or PDF)", type=["jpg", "jpeg", "png", "pdf"])
if uploaded_file:
    file_type = uploaded_file.type

    # If it's a PDF, convert first page to image
    if file_type == "application/pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(uploaded_file.read())
            doc = fitz.open(tmp_pdf.name)
            pix = doc[0].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    else:
        img = Image.open(uploaded_file)

    st.image(img, caption="Uploaded OMR", use_column_width=True)

    st.info("🛠️ (Auto reading of marked bubbles will be implemented here)")
    st.warning("⚠️ Currently simulated answers are used. You'll need to integrate OpenCV-based bubble detection.")

    # Simulated marked answers (for demo)
    marked_answers = ["C", "C", "C", "A", "D", "B", "C", "D", "A", "B"] + [""] * 190  # 10 attempted, 190 unattempted

    # Score calculation
    score = 0
    correct, wrong, unattempted = 0, 0, 0
    for i, (marked, correct_ans) in enumerate(zip(marked_answers, answer_key), 1):
        if marked == "":
            unattempted += 1
        elif marked == correct_ans:
            score += 4
            correct += 1
        else:
            score -= 1
            wrong += 1

    st.subheader("📊 Result Summary")
    st.write(f"✅ Correct Answers: {correct}")
    st.write(f"❌ Wrong Answers: {wrong}")
    st.write(f"⭕ Unattempted: {unattempted}")
    st.write(f"🎯 Total Score: {score} / {len(answer_key) * 4}")
