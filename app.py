import streamlit as st
from google import genai
from google.genai import types
from fpdf import FPDF

# 1. SETUP
st.set_page_config(page_title="Veda Career Bridge", page_icon="🧭")
st.title("🧭 Veda Career Bridge")

with st.sidebar:
    st.header("🔑 Settings")
    api_key = st.text_input("Google API Key", type="password")

# 2. UI INPUTS
current_job = st.text_input("Current Profession", "e.g., ICU Nurse or Sales Rep")
target_role = st.text_input("Target 2026 Role", "e.g., Clinical Product Manager")

# 3. DYNAMIC PROMPT LOGIC
def build_custom_prompt(curr, target):
    base = f"Analyze transition from {curr} to {target}. Find 2 real 2026 job listings."
    if "nurse" in curr.lower():
        return base + " Focus on flipping clinical triage to product prioritization."
    if "sales" in curr.lower():
        return base + " Focus on moving from cold calling to AI-automated RevOps."
    return base

# 4. EXECUTION
if st.button("🚀 Generate Bridge Report"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    else:
        try:
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

            # Show Result
            report_text = response.text
            st.markdown(report_text)
            
# --- 4. EXECUTION (FIXED ALIGNMENT) ---
if st.button("🚀 Generate Bridge Report"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    else:
        try:
            # The risky AI action
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

            # Show Result
            report_text = response.text
            st.markdown(report_text)

            # PDF Download logic
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            pdf.cell(200, 10, txt="Veda Career Bridge: Official Report", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=report_text)
            
            pdf_bytes = pdf.output()
            st.download_button("📥 Download PDF Report", data=pdf_bytes, file_name="Career_Pivot.pdf")

        except Exception as e:
            # This is the "safety net" that fixes your error
            st.error(f"Something went wrong: {e}")
        
        except Exception as e:
            st.error(f"Something went wrong: {e}")
