import re
import ast
from typing import Dict, List, Any

class AISuggestor:
    """
    Provides intelligent rule-based suggestions for code improvement
    """
    
    def __init__(self):
        self.suggestions = []
    
    def get_suggestions(self, code: str, errors: Dict[str, List]) -> Dict[str, Any]:
        """
        Generate intelligent suggestions based on code and detected errors
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            Dictionary containing analysis and suggestions
        """
        analysis = self._analyze_code(code, errors)
        improvements = self._generate_improvements(code, errors)
        refactored_code = self._refactor_code(code, errors)
        
        return {
            'analysis': analysis,
            'improvements': improvements,
            'refactored_code': refactored_code
        }
    
    def _analyze_code(self, code: str, errors: Dict[str, List]) -> str:
        """
        Provide high-level analysis of the code
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            Analysis string in markdown format
        """
        lines = [line for line in code.split('\n') if line.strip()]
        num_lines = len(lines)
        num_functions = code.count('def ')
        num_classes = code.count('class ')
        num_comments = sum(1 for line in code.split('\n') if line.strip().startswith('#'))
        
        analysis_parts = []
        
        # Header
        analysis_parts.append("## 📊 Code Analysis Report\n")
        
        # Basic statistics
        analysis_parts.append("### Code Statistics")
        analysis_parts.append(f"- **Total Lines of Code:** {num_lines}")
        analysis_parts.append(f"- **Functions Defined:** {num_functions}")
        analysis_parts.append(f"- **Classes Defined:** {num_classes}")
        analysis_parts.append(f"- **Comments:** {num_comments}")
        analysis_parts.append("")
        
        # Issue summary
        total_issues = len(errors.get('unused_vars', [])) + len(errors.get('unused_imports', []))
        
        analysis_parts.append("### Issues Detected")
        if total_issues > 0:
            analysis_parts.append(f"- **Total Issues Found:** {total_issues}")
            analysis_parts.append(f"  - Unused Imports: {len(errors.get('unused_imports', []))}")
            analysis_parts.append(f"  - Unused Variables: {len(errors.get('unused_vars', []))}")
        else:
            analysis_parts.append("✅ **No issues detected!** Your code is clean.")
        
        analysis_parts.append("")
        
        # Code quality assessment
        quality_score = self._calculate_quality_score(code, errors)
        analysis_parts.append("### Code Quality Assessment")
        analysis_parts.append(f"**Overall Score:** {quality_score}/100")
        analysis_parts.append("")
        
        # Quality breakdown
        if quality_score >= 90:
            analysis_parts.append("🌟 **Excellent!** Your code follows best practices.")
        elif quality_score >= 75:
            analysis_parts.append("👍 **Good!** Your code quality is solid with minor areas for improvement.")
        elif quality_score >= 60:
            analysis_parts.append("⚠️ **Fair.** Consider implementing the suggested improvements.")
        else:
            analysis_parts.append("⚠️ **Needs Improvement.** Please review the suggestions below.")
        
        analysis_parts.append("")
        
        # Additional insights
        analysis_parts.append("### Key Insights")
        insights = self._generate_insights(code, errors, num_lines, num_functions)
        for insight in insights:
            analysis_parts.append(f"- {insight}")
        
        return '\n'.join(analysis_parts)
    
    def _generate_insights(self, code: str, errors: Dict[str, List], 
                          num_lines: int, num_functions: int) -> List[str]:
        """
        Generate insights about the code
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            num_lines: Number of lines in code
            num_functions: Number of functions
            
        Returns:
            List of insight strings
        """
        insights = []
        
        # Documentation insights
        has_docstrings = '"""' in code or "'''" in code
        if has_docstrings:
            insights.append("✅ Code includes docstrings for documentation")
        elif num_functions > 0:
            insights.append("📝 Consider adding docstrings to improve documentation")
        
        # Type hints
        has_type_hints = '->' in code or ': str' in code or ': int' in code or ': List' in code
        if has_type_hints:
            insights.append("✅ Type hints detected - great for code clarity!")
        elif num_functions > 1:
            insights.append("💡 Type hints could improve code maintainability")
        
        # Error handling
        has_try_except = 'try:' in code and 'except' in code
        if has_try_except:
            insights.append("✅ Error handling implemented")
        elif num_lines > 20:
            insights.append("🛡️ Consider adding error handling for robustness")
        
        # Code organization
        if num_functions > 10:
            insights.append("📦 Large number of functions - consider organizing into classes or modules")
        
        # Line length
        long_lines = [line for line in code.split('\n') if len(line) > 100]
        if len(long_lines) > 3:
            insights.append(f"📏 {len(long_lines)} lines exceed 100 characters - consider breaking them up")
        
        # Complexity
        complexity = self._estimate_complexity(code)
        if complexity > 20:
            insights.append("🔄 High complexity detected - consider refactoring into smaller functions")
        
        return insights
    
    def _estimate_complexity(self, code: str) -> int:
        """
        Estimate code complexity using simple heuristics
        
        Args:
            code: Python code string
            
        Returns:
            Complexity score
        """
        try:
            tree = ast.parse(code)
            complexity = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    complexity += 1
                elif isinstance(node, ast.FunctionDef):
                    complexity += 2
                elif isinstance(node, ast.ClassDef):
                    complexity += 3
                elif isinstance(node, (ast.Try, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(node, ast.Lambda):
                    complexity += 1
            
            return complexity
        except:
            return 0
    
    def _calculate_quality_score(self, code: str, errors: Dict[str, List]) -> int:
        """
        Calculate a comprehensive quality score for the code
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            Quality score (0-100)
        """
        score = 100
        
        # Deduct for unused imports (5 points each)
        score -= len(errors.get('unused_imports', [])) * 5
        
        # Deduct for unused variables (5 points each)
        score -= len(errors.get('unused_vars', [])) * 5
        
        # Deduct for lack of docstrings
        num_functions = code.count('def ')
        has_docstrings = '"""' in code or "'''" in code
        if num_functions > 0 and not has_docstrings:
            score -= 10
        
        # Deduct for long lines
        lines = code.split('\n')
        long_lines = sum(1 for line in lines if len(line) > 100)
        score -= min(long_lines * 2, 15)
        
        # Deduct for lack of error handling
        has_try_except = 'try:' in code and 'except' in code
        if len(lines) > 20 and not has_try_except:
            score -= 5
        
        # Bonus for type hints
        if '->' in code or ': str' in code or ': int' in code:
            score = min(100, score + 5)
        
        # Bonus for comments
        num_comments = sum(1 for line in lines if line.strip().startswith('#'))
        if num_comments >= len(lines) * 0.1:  # At least 10% comments
            score = min(100, score + 5)
        
        return max(0, min(100, score))
    
    def _generate_improvements(self, code: str, errors: Dict[str, List]) -> List[Dict[str, Any]]:
        """
        Generate specific improvement suggestions
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            List of improvement suggestions
        """
        improvements = []
        
        # Suggest removing unused imports
        if errors.get('unused_imports'):
            imports_list = ', '.join([f"`{imp['name']}`" for imp in errors['unused_imports'][:5]])
            more = ''
            if len(errors['unused_imports']) > 5:
                more = f" and {len(errors['unused_imports']) - 5} more"
            
            improvements.append({
                'title': '🧹 Remove Unused Imports',
                'description': f"The following imports are not being used in your code: {imports_list}{more}. Removing them will make your code cleaner and reduce dependencies.",
                'priority': 'High',
                'code': '# Remove these import statements:\n' + '\n'.join(
                    [f"# Line {imp['line']}: import {imp['name'].split('.')[-1]}" 
                     for imp in errors['unused_imports'][:5]]
                )
            })
        
        # Suggest handling unused variables
        if errors.get('unused_vars'):
            vars_list = ', '.join([f"`{var['name']}`" for var in errors['unused_vars'][:5]])
            more = ''
            if len(errors['unused_vars']) > 5:
                more = f" and {len(errors['unused_vars']) - 5} more"
            
            improvements.append({
                'title': '🔧 Handle Unused Variables',
                'description': f"Variables {vars_list}{more} are assigned but never used. Either use them in your logic or remove them. If they're intentionally unused (like in unpacking), prefix them with an underscore.",
                'priority': 'Medium',
                'code': '''# For intentionally unused variables:
_, value = some_tuple  # Use underscore for unused values

# Or simply remove if not needed:
# unused_var = 10  # Remove this line'''
            })
        
        # Suggest adding docstrings
        num_functions = code.count('def ')
        has_docstrings = '"""' in code or "'''" in code
        if num_functions > 0 and not has_docstrings:
            improvements.append({
                'title': '📝 Add Docstrings',
                'description': 'Your code has functions but no docstrings. Adding docstrings helps other developers (and future you) understand what each function does.',
                'priority': 'Medium',
                'code': '''def calculate_sum(a: int, b: int) -> int:
    """
    Calculate the sum of two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b'''
            })
        
        # Suggest type hints
        if num_functions > 0 and '->' not in code:
            improvements.append({
                'title': '🎯 Add Type Hints',
                'description': 'Type hints make your code more readable and help catch type-related bugs early. Modern Python encourages their use.',
                'priority': 'Low',
                'code': '''# Without type hints:
def greet(name):
    return f"Hello, {name}"

# With type hints:
def greet(name: str) -> str:
    return f"Hello, {name}"'''
            })
        
        # Check for long functions
        lines = code.split('\n')
        function_lengths = self._get_function_lengths(code)
        long_functions = [f for f in function_lengths if function_lengths[f] > 50]
        
        if long_functions:
            improvements.append({
                'title': '✂️ Break Down Large Functions',
                'description': f"Functions {', '.join([f'`{f}`' for f in long_functions[:3]])} are quite long. Consider breaking them into smaller, focused functions following the Single Responsibility Principle.",
                'priority': 'Medium',
                'code': '''# Instead of one large function:
def process_data(data):
    # 50+ lines of code...
    pass

# Break into smaller functions:
def validate_data(data):
    # Validation logic
    pass

def transform_data(data):
    # Transformation logic
    pass

def save_data(data):
    # Saving logic
    pass'''
            })
        
        # Check for error handling
        has_try_except = 'try:' in code and 'except' in code
        if len(lines) > 20 and not has_try_except:
            improvements.append({
                'title': '🛡️ Add Error Handling',
                'description': 'Your code lacks error handling. Adding try-except blocks will make it more robust and prevent unexpected crashes.',
                'priority': 'Medium',
                'code': '''try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error occurred: {e}")
    result = default_value
except Exception as e:
    print(f"Unexpected error: {e}")
    raise'''
            })
        
        return improvements
    
    def _get_function_lengths(self, code: str) -> Dict[str, int]:
        """
        Calculate the length of each function in the code
        
        Args:
            code: Python code string
            
        Returns:
            Dictionary mapping function names to their lengths
        """
        function_lengths = {}
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Count non-empty, non-comment lines in function
                    func_start = node.lineno
                    func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start + 10
                    length = func_end - func_start
                    function_lengths[node.name] = length
        except:
            pass
        
        return function_lengths
    
    def _refactor_code(self, code: str, errors: Dict[str, List]) -> str:
        """
        Generate refactored version of the code with improvements applied
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            Refactored code string
        """
        refactored = code
        lines = refactored.split('\n')
        
        # Get line numbers of unused imports
        unused_import_lines = set(imp['line'] - 1 for imp in errors.get('unused_imports', []))
        
        # Remove or comment out unused imports
        cleaned_lines = []
        for i, line in enumerate(lines):
            if i in unused_import_lines:
                # Comment out instead of removing to show what was changed
                if line.strip():
                    cleaned_lines.append(f"# REMOVED (unused): {line.strip()}")
            else:
                cleaned_lines.append(line)
        
        refactored = '\n'.join(cleaned_lines)
        
        # Comment out unused variables
        for var in errors.get('unused_vars', []):
            var_name = var['name']
            # Use word boundaries to avoid partial matches
            pattern = rf'(\s*)({re.escape(var_name)}\s*=)'
            replacement = r'\1# UNUSED: \2'
            refactored = re.sub(pattern, replacement, refactored, count=1)
        
        # Add a header comment explaining the refactoring
        if errors.get('unused_imports') or errors.get('unused_vars'):
            header = [
                "# ====================================",
                "# REFACTORED CODE",
                "# Changes made:",
            ]
            
            if errors.get('unused_imports'):
                header.append(f"# - Removed {len(errors['unused_imports'])} unused import(s)")
            
            if errors.get('unused_vars'):
                header.append(f"# - Marked {len(errors['unused_vars'])} unused variable(s)")
            
            header.append("# ====================================\n")
            refactored = '\n'.join(header) + '\n' + refactored
        
        return refactored
