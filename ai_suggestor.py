import re
from typing import Dict, List, Any

class AISuggestor:
    """
    Provides AI-powered suggestions for code improvement
    """
    
    def __init__(self):
        self.suggestions = []
    
    def get_suggestions(self, code: str, errors: Dict[str, List]) -> Dict[str, Any]:
        """
        Generate AI-powered suggestions based on code and detected errors
        
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
            Analysis string
        """
        lines = code.split('\n')
        num_lines = len(lines)
        num_functions = code.count('def ')
        num_classes = code.count('class ')
        
        analysis_parts = []
        
        # Basic stats
        analysis_parts.append(f"**Code Statistics:**")
        analysis_parts.append(f"- Total Lines: {num_lines}")
        analysis_parts.append(f"- Functions: {num_functions}")
        analysis_parts.append(f"- Classes: {num_classes}")
        analysis_parts.append("")
        
        # Error summary
        total_issues = len(errors.get('unused_vars', [])) + len(errors.get('unused_imports', []))
        
        if total_issues > 0:
            analysis_parts.append(f"**Issues Found:** {total_issues}")
            analysis_parts.append(f"- Unused imports: {len(errors.get('unused_imports', []))}")
            analysis_parts.append(f"- Unused variables: {len(errors.get('unused_vars', []))}")
        else:
            analysis_parts.append("**Status:** ✅ No major issues detected!")
        
        analysis_parts.append("")
        
        # Code quality assessment
        quality_score = self._calculate_quality_score(code, errors)
        analysis_parts.append(f"**Code Quality Score:** {quality_score}/100")
        
        if quality_score >= 80:
            analysis_parts.append("Your code quality is excellent!")
        elif quality_score >= 60:
            analysis_parts.append("Your code quality is good, with room for minor improvements.")
        else:
            analysis_parts.append("Consider implementing the suggested improvements below.")
        
        return '\n'.join(analysis_parts)
    
    def _calculate_quality_score(self, code: str, errors: Dict[str, List]) -> int:
        """
        Calculate a quality score for the code
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            Quality score (0-100)
        """
        score = 100
        
        # Deduct points for errors
        score -= len(errors.get('unused_imports', [])) * 5
        score -= len(errors.get('unused_vars', [])) * 5
        
        # Deduct points for lack of docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            score -= 10
        
        # Deduct points for very long lines
        lines = code.split('\n')
        long_lines = sum(1 for line in lines if len(line) > 100)
        score -= min(long_lines * 2, 15)
        
        # Bonus for type hints
        if '->' in code or ': str' in code or ': int' in code:
            score += 5
        
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
            imports_list = ', '.join([imp['name'] for imp in errors['unused_imports'][:3]])
            improvements.append({
                'title': 'Remove Unused Imports',
                'description': f"Remove unused imports: {imports_list}",
                'priority': 'high',
                'code': '# Remove these import statements:\n' + '\n'.join(
                    [f"# Line {imp['line']}: {imp['name']}" for imp in errors['unused_imports']]
                )
            })
        
        # Suggest removing unused variables
        if errors.get('unused_vars'):
            vars_list = ', '.join([var['name'] for var in errors['unused_vars'][:3]])
            improvements.append({
                'title': 'Remove or Use Unused Variables',
                'description': f"Variables {vars_list} are assigned but never used. Consider removing them or using them in your logic.",
                'priority': 'medium'
            })
        
        # Suggest adding docstrings
        if 'def ' in code:
            has_docstrings = '"""' in code or "'''" in code
            if not has_docstrings:
                improvements.append({
                    'title': 'Add Docstrings',
                    'description': 'Add docstrings to your functions to improve code documentation.',
                    'priority': 'medium',
                    'code': '''def example_function(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    # function body
    pass'''
                })
        
        # Suggest type hints
        if 'def ' in code and '->' not in code:
            improvements.append({
                'title': 'Add Type Hints',
                'description': 'Consider adding type hints to improve code clarity and catch type-related bugs.',
                'priority': 'low',
                'code': '''def example(name: str, age: int) -> str:
    return f"{name} is {age} years old"'''
            })
        
        # Check for long functions
        lines = code.split('\n')
        in_function = False
        function_length = 0
        for line in lines:
            if line.strip().startswith('def '):
                in_function = True
                function_length = 0
            elif in_function:
                if line.strip() and not line.strip().startswith('#'):
                    function_length += 1
                if line.strip().startswith('def ') or line.strip().startswith('class '):
                    in_function = False
        
        if function_length > 50:
            improvements.append({
                'title': 'Consider Breaking Down Large Functions',
                'description': 'Some functions are quite long. Consider breaking them into smaller, more focused functions.',
                'priority': 'medium'
            })
        
        return improvements
    
    def _refactor_code(self, code: str, errors: Dict[str, List]) -> str:
        """
        Generate refactored version of the code
        
        Args:
            code: Python code string
            errors: Dictionary of detected errors
            
        Returns:
            Refactored code string
        """
        refactored = code
        
        # Remove unused imports
        lines = refactored.split('\n')
        unused_import_lines = set(imp['line'] - 1 for imp in errors.get('unused_imports', []))
        
        cleaned_lines = []
        for i, line in enumerate(lines):
            if i not in unused_import_lines:
                cleaned_lines.append(line)
            else:
                cleaned_lines.append(f"# REMOVED: {line.strip()} (unused import)")
        
        refactored = '\n'.join(cleaned_lines)
        
        # Comment out unused variables
        for var in errors.get('unused_vars', []):
            var_name = var['name']
            # Use word boundaries to avoid partial matches
            pattern = rf'\b{re.escape(var_name)}\s*='
            refactored = re.sub(
                pattern,
                f'# UNUSED: {var_name} =',
                refactored,
                count=1
            )
        
        return refactored
