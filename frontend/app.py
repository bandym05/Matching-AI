import streamlit as st
import requests

st.title("🆔 Face Match Verification Demo")

id_image = st.file_uploader("Upload ID Card Image", type=["jpg", "jpeg", "png"])
selfie_image = st.file_uploader("Upload Selfie or Headshot", type=["jpg", "jpeg", "png"])

if st.button("Compare Faces") and id_image and selfie_image:
    with st.spinner("Comparing..."):
        files = {
            "id_image": id_image,
            "selfie_image": selfie_image,
        }
        response = requests.post("http://localhost:8000/compare", files=files)
        data = response.json()

        if data["success"]:
            st.success(f"Confidence Score: {data['confidence']}")
            if data["match"]:
                st.markdown("✅ **Match Detected!**")
            else:
                st.markdown("❌ **Faces do not match.**")
        else:
            st.error(data["message"])
