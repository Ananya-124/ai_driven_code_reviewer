import ast
from typing import Dict, List, Any

class ErrorDetector:
    """
    Detects unused variables and imports
    """
    
    def detect_errors(self, code: str, ast_tree: ast.AST = None) -> Dict[str, List]:
        """
        Detect unused variables and imports
        
        Args:
            code: Python code string
            ast_tree: Optional pre-parsed AST tree
            
        Returns:
            Dictionary containing lists of errors
        """
        if ast_tree is None:
            try:
                ast_tree = ast.parse(code)
            except:
                return {'unused_vars': [], 'unused_imports': []}
        
        unused_vars = self._find_unused_variables(ast_tree)
        unused_imports = self._find_unused_imports(ast_tree)
        
        return {
            'unused_vars': unused_vars,
            'unused_imports': unused_imports
        }
    
    def _find_unused_variables(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Find variables that are assigned but never used"""
        assigned = {}
        used = set()
        
        # Collect assignments
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if not target.id.startswith('_'):
                            assigned[target.id] = node.lineno
        
        # Collect usages
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used.add(node.id)
        
        # Find unused
        unused = []
        for var_name, line_no in assigned.items():
            if var_name not in used:
                unused.append({
                    'name': var_name,
                    'line': line_no
                })
        
        return unused
    
    def _find_unused_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Find imports that are never used"""
        imported = {}
        used = set()
        
        # Collect imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name.split('.')[0]
                    imported[name] = {
                        'full_name': alias.name,
                        'line': node.lineno
                    }
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name != '*':
                        name = alias.asname if alias.asname else alias.name
                        imported[name] = {
                            'full_name': f"{node.module}.{alias.name}" if node.module else alias.name,
                            'line': node.lineno
                        }
        
        # Collect usages
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    used.add(node.value.id)
        
        # Find unused
        unused = []
        for name, info in imported.items():
            if name not in used:
                unused.append({
                    'name': info['full_name'],
                    'line': info['line']
                })
        
        return unused
