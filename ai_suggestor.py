from typing import Dict, List

class AISuggestor:
    """
    Provides simple AI-powered suggestions for code improvement
    """
    
    def get_suggestions(self, code: str, errors: Dict[str, List], parse_result: Dict) -> str:
        """
        Generate suggestions based on code and errors
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            parse_result: Result from code parser
            
        Returns:
            Formatted suggestion string
        """
        suggestions = []
        
        # If there are syntax errors
        if not parse_result['success']:
            suggestions.append("**🔴 Fix Syntax Errors First**")
            suggestions.append(f"- {parse_result['error']}")
            suggestions.append("\nOnce syntax errors are fixed, I can provide more suggestions!")
            return '\n'.join(suggestions)
        
        # Check for unused imports
        if errors.get('unused_imports'):
            suggestions.append("**🧹 Clean Up Imports**")
            for imp in errors['unused_imports'][:3]:
                suggestions.append(f"- Remove unused import: `{imp['name']}` (line {imp['line']})")
            if len(errors['unused_imports']) > 3:
                suggestions.append(f"- ...and {len(errors['unused_imports']) - 3} more")
            suggestions.append("")
        
        # Check for unused variables
        if errors.get('unused_vars'):
            suggestions.append("**🔧 Remove Unused Variables**")
            for var in errors['unused_vars'][:3]:
                suggestions.append(f"- Variable `{var['name']}` is never used (line {var['line']})")
            if len(errors['unused_vars']) > 3:
                suggestions.append(f"- ...and {len(errors['unused_vars']) - 3} more")
            suggestions.append("")
        
        # General suggestions
        suggestions.append("**💡 General Improvements**")
        
        # Check for docstrings
        if 'def ' in code and '"""' not in code:
            suggestions.append("- Add docstrings to explain what your functions do")
        
        # Check for type hints
        if 'def ' in code and '->' not in code:
            suggestions.append("- Consider adding type hints for better code clarity")
        
        # Check for comments
        num_lines = len(code.split('\n'))
        num_comments = sum(1 for line in code.split('\n') if line.strip().startswith('#'))
        if num_lines > 10 and num_comments == 0:
            suggestions.append("- Add comments to explain complex logic")
        
        # If no issues found
        if not errors.get('unused_imports') and not errors.get('unused_vars'):
            if len(suggestions) == 1:  # Only "General Improvements" header
                suggestions.append("✅ Your code looks good!")
        
        return '\n'.join(suggestions)
