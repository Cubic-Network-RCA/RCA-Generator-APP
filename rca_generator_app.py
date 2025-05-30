import streamlit as st
import openai
import os

# Set your OpenAI API key here or use environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this as a secret in Streamlit Cloud

st.set_page_config(page_title="AI-Powered RCA Generator")
st.title("🚨 Major Incident RCA Generator")

st.markdown("""
Paste your **incident timeline** below. This tool will analyze the events and generate a full RCA in your company's official format.
""")

# Text input area
timeline = st.text_area("📋 Paste Timeline Here", height=300)

# Submit button
if st.button("Generate RCA"):
    if not timeline.strip():
        st.warning("Please paste a timeline before generating the RCA.")
    else:
        with st.spinner("Generating RCA..."):
            prompt = f"""
You are a network operations engineer. Based on the following incident timeline, generate a full RCA (Root Cause Analysis) report using this structure:

- Incident Date
- Incident / Problem Reference (use placeholder INC-XXXX)
- Start Time (UTC)
- Service Restoration (UTC)
- End Time (UTC)
- Services Affected
- Customer Impact
- Description
- Root Cause
- Workaround (Actions to restore service)
- Long Term Solutions (Actions to prevent recurrence with owner, status, and date)

Timeline:
"""
            prompt += timeline.strip()

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert in writing RCA reports for network incidents."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

                rca_text = response["choices"][0]["message"]["content"]
                st.success("RCA Generated Successfully!")
                st.text_area("📄 Generated RCA", value=rca_text, height=500)
            except Exception as e:
                st.error(f"Error generating RCA: {str(e)}")

st.markdown("---")
st.markdown("Developed for Cubic AI Day 2025 ✨")
