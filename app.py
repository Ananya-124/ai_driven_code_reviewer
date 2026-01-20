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
st.markdown("Paste your Python code below for instant analysis and suggestions")

# Initialize components
parser = CodeParser()
detector = ErrorDetector()
suggestor = AISuggestor()

# Code input
code_input = st.text_area(
    "Python Code:",
    height=300,
    placeholder="# Paste your Python code here...\n\ndef example():\n    import os\n    x = 10\n    return 5"
)

# Analyze button
if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
    if code_input.strip():
        with st.spinner("Analyzing..."):
            # Parse code
            parse_result = parser.parse_code(code_input)
            
            # Detect errors (even if parsing fails)
            if parse_result['success']:
                errors = detector.detect_errors(code_input, parse_result['ast'])
            else:
                errors = {'unused_vars': [], 'unused_imports': []}
            
            # Show results in two columns
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 Analysis Results")
                
                # Show parsing status
                if parse_result['success']:
                    st.success("✅ Code parsed successfully")
                else:
                    st.error(f"❌ Syntax Error: {parse_result['error']}")
                
                # Show issues
                total_issues = len(errors['unused_vars']) + len(errors['unused_imports'])
                
                if total_issues > 0:
                    st.warning(f"⚠️ Found {total_issues} issue(s)")
                    
                    if errors['unused_imports']:
                        st.write("**Unused Imports:**")
                        for imp in errors['unused_imports']:
                            st.code(f"Line {imp['line']}: {imp['name']}")
                    
                    if errors['unused_vars']:
                        st.write("**Unused Variables:**")
                        for var in errors['unused_vars']:
                            st.code(f"Line {var['line']}: {var['name']}")
                else:
                    if parse_result['success']:
                        st.success("🎉 No issues found!")
            
            with col2:
                st.subheader("💡 AI Suggestions")
                
                # Get suggestions
                suggestions = suggestor.get_suggestions(code_input, errors, parse_result)
                
                # Display suggestions
                st.markdown(suggestions)
    else:
        st.warning("⚠️ Please enter some code to analyze")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Paste code → Get instant feedback")
