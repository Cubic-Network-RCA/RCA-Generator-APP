import streamlit as st
import openai
import os

# Azure OpenAI credentials (safely read from Streamlit secrets)
client = openai.AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://vibic3.openai.azure.com/"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-01-01-preview"  # per your company config
)

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-nano")

st.set_page_config(page_title="AI-Powered RCA Generator")
st.title("🚨 Major Incident RCA Generator")

st.markdown("""
Paste your **incident timeline** below. This tool will analyze the events and generate a full RCA in your company's official format.
""")

# Input area
timeline = st.text_area("📋 Paste Timeline Here", height=300)

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
{timeline.strip()}
"""

            try:
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": "You are an expert in writing RCA reports for network incidents."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=800
                )

                rca_output = response.choices[0].message.content
                st.success("✅ RCA Generated Successfully!")
                st.text_area("📄 Generated RCA", value=rca_output, height=500)
            except Exception as e:
                st.error(f"❌ Error generating RCA: {e}")

st.markdown("---")
st.markdown("Developed for Cubic AI Day 2025 ✨")
