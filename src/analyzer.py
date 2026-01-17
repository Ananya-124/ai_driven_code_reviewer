import ast
from radon.complexity import cc_visit

def analyze_code(code):
    results = {
        "syntax_ok": True,
        "error": None,
        "complexity": []
    }
    
    # 1. Check Syntax
    try:
        ast.parse(code)
    except SyntaxError as e:
        results["syntax_ok"] = False
        results["error"] = f"Line {e.lineno}: {e.msg}"
        return results # Exit early if code can't be parsed

    # 2. Check Complexity (Cyclomatic Complexity)
    try:
        # cc_visit returns a list of objects representing functions/classes
        complexity_blocks = cc_visit(code)
        for block in complexity_blocks:
            results["complexity"].append({
                "type": type(block).__name__,
                "name": block.name,
                "score": block.complexity,
                "rank": block.letter_rank() # A (simple) to F (complex)
            })
    except Exception as e:
        results["error"] = f"Complexity Analysis Error: {str(e)}"
        
    return results