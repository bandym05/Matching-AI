import streamlit as st
import requests
import numpy as np

st.title("🆔 Face Match Verification")

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

if st.button("Extract Text from ID") and id_image:
    with st.spinner("Extracting text..."):
        files = {"id_image": id_image}
        response = requests.post("http://localhost:8000/extract-text", files=files)
        
        try:
            data = response.json()
        except Exception as e:
            st.error("❌ Failed to parse JSON response.")
            st.error(f"Error: {e}")
            st.write(f"Raw response: {response.text}")
            st.stop()

        if data.get("success"):
            extracted = data["data"]
            st.subheader("📝 Extracted ID Information")
            st.write(f"**Name:** {extracted['name']}")
            st.write(f"**ID Number:** {extracted['id_number']}")
            st.write(f"**Date of Birth:** {extracted['dob']}")
            st.write(f"**Nationality:** {extracted['nationality']}")
            st.expander("🔍 Raw Text").write(extracted["raw_text"])
        else:
            st.error("❌ Failed to extract text from the image.")
            st.write(f"Error message from server: {data.get('message')}")
