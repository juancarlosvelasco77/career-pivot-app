import streamlit as st
from google import genai
from google.genai import types
from fpdf import FPDF

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Veda: Career Bridge", page_icon="🧭", layout="centered")
st.title("🧭 Veda Career Bridge")
st.markdown("### Your 2026 AI-Powered Career Pivot Agent")

# Sidebar for the API Key
with st.sidebar:
    st.header("🔑 Authentication")
    api_key = st.text_input("Enter Google API Key", type="password")
    st.info("Don't have a key? Get one for free at aistudio.google.com")

# --- 2. USER INPUTS ---
col1, col2 = st.columns(2)
with col1:
    current_job = st.text_input("Current Profession", "K-12 Teacher")
with col2:
    target_role = st.text_input("Dream Pivot", "EdTech Architect")

# --- 3. THE AI AGENT LOGIC ---
if st.button("🚀 Build My Bridge"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar to begin.")
    else:
        try:
            # Initialize the Gemini 3 Client
            client = genai.Client(api_key=api_key)
            
            with st.status("🔍 Veda is searching the live 2026 job market...", expanded=True) as status:
                # Enable Google Search Grounding for real-time accuracy
                search_tool = types.Tool(google_search=types.GoogleSearch())
                
                # Define the prompt for the 3.0 model
                prompt = f"""
                Analyze the transition from {current_job} to {target_role}. 
                1. Find 2 actual companies currently hiring for this role in 2026.
                2. Translate 3 specific skills from {current_job} into {target_role} terminology.
                3. Provide a 30-day micro-learning roadmap.
                """
                
                # Generate content using Gemini 3 Pro
                response = client.models.generate_content(
                    model="gemini-3-pro-preview", 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[search_tool],
                        thinking_config=types.ThinkingConfig(thinking_level="high")
                    )
                )
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

            # Display the AI's response
            report_text = response.text
            st.subheader("Your Personalized Bridge Report")
            st.markdown(report_text)

            # --- 4. PDF GENERATION ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Veda Career Bridge: Official Report", ln=True, align='C')
            pdf.ln(10)
            # multi_cell handles long text wrapping
            pdf.multi_cell(0, 10, txt=report_text.encode('latin-1', 'ignore').decode('latin-1'))
            
            # Create a download button for the PDF
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="📥 Download Full PDF Roadmap",
                data=pdf_bytes,
                file_name="Career_Pivot_Plan.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error: {e}. Check if your API Key is valid and active.")

# --- 5. FOOTER ---
st.divider()
st.caption("Powered by Gemini 3.0 Pro & Google Search Grounding.")
