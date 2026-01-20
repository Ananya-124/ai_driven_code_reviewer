
from src.analyzer import analyze_code
from src.ai_engine import get_ai_review
# from st_diff_viewer import diff_viewer
import streamlit as st

st.set_page_config(
    page_title="Ai Driven Code Reviewer",
    page_icon="🔎",
    layout="wide"
)

# --- CLEAN CSS (Normal Sidebar, Custom IDE Editor) ---
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #ffffff;
    }
    
    /* Code Editor Styling (Dark IDE look) */
    .stTextArea textarea {
        font-family: 'Source Code Pro', monospace;
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        border-radius: 8px;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = None

# --- UI Header ---
st.title("📔 Ai Code Reviewer")
st.subheader("Paste your code below to get a Review")

# --- Code Editor ---
code_input = st.text_area(
    label="Code Editor",
    placeholder="Paste your code here...",
    height=250,
    label_visibility="collapsed"
)

# --- Normal Sidebar ---
# Removed the custom CSS for sidebar, so it uses default Streamlit styling
language = st.sidebar.selectbox("Select Language", ["Python", "Java", "C++", "JavaScript"])
st.sidebar.divider()
st.sidebar.info("Select your language and hit Analyze to start the audit.")

# --- Action Button ---
if st.button("Analyze Code"):
    if code_input.strip():
        # Static Analysis for Python
        if language == "Python":
            report = analyze_code(code_input)
            if not report["syntax_ok"]:
                st.error(f"⚠️ Python Syntax Error: {report['error']}")
                st.stop()
           
        
        # AI Analysis
        with st.spinner(f"🤖 Analysing Your {language} code..."):
            # st.session_state.ai_feedback = get_ai_review(code_input) 
            st.write_stream(get_ai_review(code_input))
    else:
        st.warning("Please enter some code first.")

# --- DISPLAY RESULTS ---
if st.session_state.ai_feedback:
    feedback = st.session_state.ai_feedback
    
    if "[ERRORS]" in feedback and "[SUGGESTIONS]" in feedback:
        try:
            # Parsing the logic
            parts = feedback.split("[ERRORS]")[1].split("[SUGGESTIONS]")
            error_content = parts[0]
            
            parts = parts[1].split("[COMPLEXITY]")
            suggestion_content = parts[0]
            
            parts = parts[1].split("[FIXED_CODE]")
            complexity_content = parts[0]
            fixed_code = parts[1].strip().replace("```python", "").replace("```", "").replace("```javascript", "").replace("```java", "").replace("```cpp", "")
            
            # Create Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🚨 ERROR LOG", "💡 SUGGESTIONS", "📊 COMPLEXITY", "🛠️ AUTO-FIX"])

            with tab1:
                st.markdown("### Detected Issues")
                st.markdown(error_content)

            with tab2:
                st.markdown("### Improvement Suggestions")
                st.markdown(suggestion_content)

            with tab3:
                st.markdown("### Algorithm Analysis")
                st.markdown(complexity_content)
                
            # with tab4:
            #     st.subheader("Comparison: Original vs. Fixed")
            #     diff_viewer(code_input, fixed_code, lang=language.lower(), key="main_diff_viewer")
        
        except Exception as e:
            st.error("Error parsing AI response. Showing raw feedback below.")
            st.markdown(feedback)
    else:
        st.markdown(feedback)
        

