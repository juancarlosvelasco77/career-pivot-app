import streamlit as st
from google import genai
from google.genai import types
from fpdf import FPDF

# --- 1. SETUP & UI ---
st.set_page_config(page_title="Veda Career Bridge", page_icon="🧭")
st.title("🧭 Veda Career Bridge")

with st.sidebar:
    st.header("🔑 Settings")
    api_key = st.text_input("Google API Key", type="password")

current_job = st.text_input("Current Profession", "e.g., K-12 Teacher")
target_role = st.text_input("Target 2026 Role", "e.g., EdTech Architect")

def build_custom_prompt(curr, target):
    return f"Analyze transition from {curr} to {target}. Use 2026 terminology and find 2 real jobs."

# --- 2. EXECUTION BLOCK ---
if st.button("🚀 Generate Bridge Report"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    else:
        try:
            # AI Logic
            client = genai.Client(api_key=api_key)
            search_tool = types.Tool(google_search=types.GoogleSearch())
            
            with st.status("🔍 Veda is scanning the 2026 market...", expanded=True) as status:
                final_prompt = build_custom_prompt(current_job, target_role)
                response = client.models.generate_content(
                    model="gemini-3-pro-preview", 
                    contents=final_prompt,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        thinking_config=types.ThinkingConfig(thinking_level="high")
                    )
                )
                status.update(label="✅ Analysis Complete!", state="complete")

            report_text = response.text
            st.markdown(report_text)

            # --- 3. FIXED PDF LOGIC ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            pdf.cell(200, 10, txt="Veda Career Bridge: Official Report", ln=True, align='C')
            pdf.ln(10)
            
            # Clean text for PDF compatibility
            clean_text = report_text.encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 10, txt=clean_text)
            
            # Use bytes() to ensure it is in the correct format for Streamlit
            pdf_bytes = bytes(pdf.output()) 
            
            st.download_button(
                label="📥 Download PDF Report", 
                data=pdf_bytes, 
                file_name="Career_Pivot.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            # This 'except' block fixes your SyntaxError
            st.error(f"Something went wrong: {e}")
