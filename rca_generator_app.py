import streamlit as st
import openai
import os
from fpdf import FPDF
import tempfile

# === Azure OpenAI Client Setup ===
client = openai.AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://vibic3.openai.azure.com/"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-01-01-preview"
)
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-nano")

# === App UI ===
st.set_page_config(page_title="AI-Powered RCA Generator")
st.title("🚨 Major Incident RCA Generator")

st.markdown("""
Paste your **incident timeline** below. This tool will analyze the events and generate a full RCA in your company's official format.
""")

# === Input Box ===
timeline = st.text_area("📋 Paste Timeline Here", height=300)

# === RCA Result Placeholder ===
rca_output = ""

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
                    max_tokens=1000
                )
                rca_output = response.choices[0].message.content

                # Remove footer if it exists
                for footer in ["**Prepared by:**", "**Position:**", "**Date:**"]:
                    if footer in rca_output:
                        rca_output = rca_output.split(footer)[0].strip()

                st.success("✅ RCA Generated Successfully!")
                st.text_area("📄 Generated RCA", value=rca_output, height=500)

            except Exception as e:
                st.error(f"❌ Error generating RCA: {e}")

# === PDF Download Button ===
def generate_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

if rca_output:
    pdf_path = generate_pdf(rca_output)
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📄 Download RCA as PDF",
            data=file,
            file_name="RCA_Report.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.markdown("Code Author: Devanshu Anand")
