import ast
from typing import Dict, List, Set, Any

class ErrorDetector:
    """
    Detects common code issues like unused variables and imports
    """
    
    def __init__(self):
        self.unused_vars = []
        self.unused_imports = []
    
    def detect_errors(self, code: str, ast_tree: ast.AST = None) -> Dict[str, List]:
        """
        Detect errors in the provided code
        
        Args:
            code: Python code string
            ast_tree: Optional pre-parsed AST tree
            
        Returns:
            Dictionary containing lists of detected errors
        """
        if ast_tree is None:
            try:
                ast_tree = ast.parse(code)
            except:
                return {'unused_vars': [], 'unused_imports': []}
        
        self.unused_vars = self._find_unused_variables(ast_tree)
        self.unused_imports = self._find_unused_imports(ast_tree)
        
        return {
            'unused_vars': self.unused_vars,
            'unused_imports': self.unused_imports
        }
    
    def _find_unused_variables(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Find variables that are assigned but never used
        
        Args:
            tree: AST tree
            
        Returns:
            List of unused variables with line numbers
        """
        assigned_vars = {}
        used_vars = set()
        
        # First pass: collect all assignments
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # Don't flag private variables or special names
                        if not var_name.startswith('_'):
                            assigned_vars[var_name] = node.lineno
            
            # Also check for assignments in function arguments
            elif isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if not arg.arg.startswith('_'):
                        assigned_vars[arg.arg] = node.lineno
        
        # Second pass: collect all variable usages
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)
            
            # Check for usage in function calls
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    used_vars.add(node.func.id)
        
        # Find unused variables
        unused = []
        for var_name, line_no in assigned_vars.items():
            if var_name not in used_vars:
                unused.append({
                    'name': var_name,
                    'line': line_no,
                    'type': 'unused_variable'
                })
        
        return unused
    
    def _find_unused_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Find imports that are never used in the code
        
        Args:
            tree: AST tree
            
        Returns:
            List of unused imports with line numbers
        """
        imported_names = {}
        used_names = set()
        
        # Collect all imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    # Handle dotted imports (e.g., os.path)
                    base_name = name.split('.')[0]
                    imported_names[base_name] = {
                        'full_name': alias.name,
                        'line': node.lineno
                    }
            
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == '*':
                        continue  # Skip wildcard imports
                    name = alias.asname if alias.asname else alias.name
                    imported_names[name] = {
                        'full_name': f"{node.module}.{alias.name}" if node.module else alias.name,
                        'line': node.lineno
                    }
        
        # Collect all name usages
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            
            # Check for attribute access (e.g., module.function)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)
        
        # Find unused imports
        unused = []
        for name, info in imported_names.items():
            if name not in used_names:
                unused.append({
                    'name': info['full_name'],
                    'line': info['line'],
                    'type': 'unused_import'
                })
        
        return unused
    
    def check_naming_conventions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Check if code follows PEP 8 naming conventions
        
        Args:
            tree: AST tree
            
        Returns:
            List of naming convention violations
        """
        violations = []
        
        for node in ast.walk(tree):
            # Check function names (should be snake_case)
            if isinstance(node, ast.FunctionDef):
                if not node.name.islower() or ' ' in node.name:
                    if not node.name.startswith('_'):
                        violations.append({
                            'line': node.lineno,
                            'name': node.name,
                            'type': 'function_naming',
                            'message': f"Function '{node.name}' should use snake_case"
                        })
            
            # Check class names (should be PascalCase)
            elif isinstance(node, ast.ClassDef):
                if not node.name[0].isupper():
                    violations.append({
                        'line': node.lineno,
                        'name': node.name,
                        'type': 'class_naming',
                        'message': f"Class '{node.name}' should use PascalCase"
                    })
        
        return violations
    
    def get_error_summary(self) -> str:
        """
        Get a summary of all detected errors
        
        Returns:
            String summary of errors
        """
        total_errors = len(self.unused_vars) + len(self.unused_imports)
        
        if total_errors == 0:
            return "No issues detected! Code looks clean."
        
        summary = f"Found {total_errors} issue(s):\n"
        summary += f"- {len(self.unused_imports)} unused import(s)\n"
        summary += f"- {len(self.unused_vars)} unused variable(s)\n"
        
        return summary
