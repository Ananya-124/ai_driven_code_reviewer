import streamlit as st
from code_parser import CodeParser
from error_detector import ErrorDetector
from ai_suggestor import AISuggestor

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Code Reviewer")
st.markdown("Upload your Python code for comprehensive analysis and AI-powered suggestions")

# Initialize components
parser = CodeParser()
detector = ErrorDetector()
suggestor = AISuggestor()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    analysis_depth = st.selectbox(
        "Analysis Depth",
        ["Quick", "Standard", "Deep"],
        index=1
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This tool analyzes Python code for:\n- Syntax errors\n- Unused variables/imports\n- Code quality issues\n- AI-powered improvements")

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Code Input", "📊 Analysis Results", "💡 AI Suggestions"])

with tab1:
    st.subheader("Enter or Upload Python Code")
    
    upload_option = st.radio("Input Method:", ["Type Code", "Upload File"])
    
    code_input = ""
    
    if upload_option == "Type Code":
        code_input = st.text_area(
            "Python Code:",
            height=400,
            placeholder="# Enter your Python code here...\n\ndef example():\n    x = 10\n    return x"
        )
    else:
        uploaded_file = st.file_uploader("Choose a Python file", type=['py'])
        if uploaded_file is not None:
            code_input = uploaded_file.read().decode("utf-8")
            st.code(code_input, language='python')
    
    analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

with tab2:
    st.subheader("Code Analysis Results")
    
    if analyze_button and code_input.strip():
        with st.spinner("Analyzing code..."):
            # Parse code
            parse_result = parser.parse_code(code_input)
            
            if parse_result['success']:
                st.success("✅ Code parsed successfully!")
                
                # Detect errors
                errors = detector.detect_errors(code_input, parse_result['ast'])
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Issues", len(errors['unused_vars']) + len(errors['unused_imports']))
                
                with col2:
                    st.metric("Unused Variables", len(errors['unused_vars']))
                
                with col3:
                    st.metric("Unused Imports", len(errors['unused_imports']))
                
                # Display detailed errors
                if errors['unused_imports']:
                    st.warning("⚠️ Unused Imports Detected")
                    for imp in errors['unused_imports']:
                        st.code(f"Line {imp['line']}: {imp['name']}", language='python')
                
                if errors['unused_vars']:
                    st.warning("⚠️ Unused Variables Detected")
                    for var in errors['unused_vars']:
                        st.code(f"Line {var['line']}: {var['name']}", language='python')
                
                if not errors['unused_imports'] and not errors['unused_vars']:
                    st.success("🎉 No unused imports or variables found!")
                
                # Store in session state for AI suggestions
                st.session_state['code_input'] = code_input
                st.session_state['errors'] = errors
                st.session_state['parse_result'] = parse_result
                
            else:
                st.error(f"❌ Parsing Error: {parse_result['error']}")
    
    elif analyze_button:
        st.warning("⚠️ Please enter some code to analyze")

with tab3:
    st.subheader("AI-Powered Suggestions")
    
    if 'code_input' in st.session_state and 'errors' in st.session_state:
        
        get_suggestions_button = st.button("💡 Get AI Suggestions", type="primary")
        
        if get_suggestions_button:
            with st.spinner("Generating AI suggestions..."):
                suggestions = suggestor.get_suggestions(
                    st.session_state['code_input'],
                    st.session_state['errors']
                )
                
                st.markdown("### 🤖 AI Analysis")
                st.markdown(suggestions['analysis'])
                
                if suggestions['improvements']:
                    st.markdown("### ✨ Suggested Improvements")
                    for i, improvement in enumerate(suggestions['improvements'], 1):
                        with st.expander(f"Improvement {i}: {improvement['title']}"):
                            st.markdown(improvement['description'])
                            if 'code' in improvement:
                                st.code(improvement['code'], language='python')
                
                if suggestions['refactored_code']:
                    st.markdown("### 🔄 Refactored Code")
                    st.code(suggestions['refactored_code'], language='python')
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Refactored Code",
                        data=suggestions['refactored_code'],
                        file_name="refactored_code.py",
                        mime="text/plain"
                    )
    else:
        st.info("👈 Please analyze code first in the 'Analysis Results' tab")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Claude AI")
