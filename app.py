import streamlit as st
from src.analyzer import analyze_code
from src.ai_engine import get_ai_review
from st_diff_viewer import diff_viewer

st.set_page_config(
    page_title="Ai Driven Code Reviewer",
    page_icon="🔎",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = None

# 1. Main Area Title
st.title("📔 Ai Code Reviewer")
st.subheader("Paste your code below to begin analysis")

code_input = st.text_area(
    label="Code Editor",
    placeholder="def my_function():\n    print('Hello World')",
    height=200,
    label_visibility="collapsed"
)

# Sidebar Language Selection
language = st.sidebar.selectbox("Select Language", ["Python", "Java", "C++", "JavaScript"])

if st.button("Analyze Code"):
    if code_input.strip():
        # --- CONDITIONAL STATIC ANALYSIS (Python Only) ---
        if language == "Python":
            report = analyze_code(code_input)
            if not report["syntax_ok"]:
                st.error(f"⚠️ Python Syntax Error: {report['error']}")
                st.stop() 
            else:
                st.success("✅ Python Static Analysis Passed!")
        
        # --- AI ANALYSIS ---
        with st.spinner(f"🤖 Analysing Your {language} code..."):
            st.session_state.ai_feedback = get_ai_review(code_input) 
    else:
        st.warning("Please enter some code first.")

# --- DISPLAY RESULTS (Combined logic in one block) ---
if st.session_state.ai_feedback:
    feedback = st.session_state.ai_feedback
    
    # Check if the AI followed our tagging format for the 4 tabs
    if "[ERRORS]" in feedback and "[SUGGESTIONS]" in feedback:
        try:
            # Parsing the logic safely
            parts = feedback.split("[ERRORS]")[1].split("[SUGGESTIONS]")
            error_content = parts[0]
            
            parts = parts[1].split("[COMPLEXITY]")
            suggestion_content = parts[0]
            
            parts = parts[1].split("[FIXED_CODE]")
            complexity_content = parts[0]
            fixed_code = parts[1].strip().replace("```python", "").replace("```", "").replace("```javascript", "").replace("```java", "").replace("```cpp", "")

            # Create the Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🚨 Errors", "💡 Suggestions", "📊 Complexity", "🛠️ Fixed Code"])

            with tab1:
                st.markdown("### Detected Issues")
                st.markdown(error_content)

            with tab2:
                st.markdown("### Improvement Suggestions")
                st.markdown(suggestion_content)

            with tab3:
                st.markdown("### Algorithm Analysis")
                st.markdown(complexity_content)
                
            with tab4:
                st.subheader("Comparison: Original vs. Fixed")
                # ADDED THE 'key' ARGUMENT HERE TO FIX THE DUPLICATE ID ERROR
                diff_viewer(code_input, fixed_code, lang=language.lower(), key="main_diff_viewer")
        
        except Exception as e:
            st.error("Error parsing AI response. Showing raw feedback below.")
            st.markdown(feedback)
    else:
        # Fallback if the AI didn't use the tags
        st.markdown(feedback)