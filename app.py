import streamlit as st
from src.analyzer import analyze_code

st.set_page_config(
    page_title="Ai Driven Code reviewer",
    page_icon="🔎",
    layout="wide"  # Ensures the text_area uses the full screen width
)

with st.sidebar:
    st.header("Settings")
    # Using radio buttons for clear visibility of choices
    language = st.radio(
        "Select Programming Language:",
        options=["Python", "Java", "C"],
        index=0, # Default to Python
        help="Choose the language of the code you are pasting."
    )
    
    st.divider()
    st.info(f"Currently analyzing: **{language}**")
    
# 1. Main Area Title
st.title("📔 Ai Code Reviewer")
st.subheader("Paste your code below to begin analysis")


code_input = st.text_area(
    label="Code Editor",
    placeholder="def my_function():\n    print('Hello World')",
    height=200,
    label_visibility="collapsed" # Hides the label for a cleaner 'IDE' look
)



if st.button("Analyze Code"):
    if code_input.strip():
        # Call the logic from Step 1
        report = analyze_code(code_input)
        
        if not report["syntax_ok"]:
            st.error(f"⚠️ Syntax Error Found: {report['error']}")
        else:
            st.success("✅ Syntax Check Passed!")
            
            # Display Complexity Results
            if report["complexity"]:
                st.subheader("Complexity Report (Radon)")
                for item in report["complexity"]:
                    # Create a metric or a colored text for each function/class
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"**{item['type']}**: `{item['name']}`")
                    col2.metric("Score", item["score"])
                    col3.write(f"**Rank**: {item['rank']}")
            else:
                st.info("No functions or classes found to analyze.")
    else:
        st.warning("Please paste some code first.")
