import ast
import sys
from typing import Dict, Any, Optional

class CodeParser:
    """
    Parses Python code and extracts structural information
    """
    
    def __init__(self):
        self.ast_tree = None
    
    def parse_code(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code and return AST along with metadata
        
        Args:
            code: String containing Python code
            
        Returns:
            Dictionary with parsing results
        """
        result = {
            'success': False,
            'ast': None,
            'error': None,
            'metadata': {}
        }
        
        try:
            # Parse the code into an AST
            self.ast_tree = ast.parse(code)
            result['success'] = True
            result['ast'] = self.ast_tree
            
            # Extract metadata
            result['metadata'] = self._extract_metadata(self.ast_tree)
            
        except SyntaxError as e:
            result['error'] = f"Syntax Error at line {e.lineno}: {e.msg}"
        except Exception as e:
            result['error'] = f"Parsing Error: {str(e)}"
        
        return result
    
    def _extract_metadata(self, tree: ast.AST) -> Dict[str, Any]:
        """
        Extract metadata from AST
        
        Args:
            tree: AST tree
            
        Returns:
            Dictionary containing code metadata
        """
        metadata = {
            'functions': [],
            'classes': [],
            'imports': [],
            'variables': [],
            'total_lines': 0
        }
        
        for node in ast.walk(tree):
            # Extract function definitions
            if isinstance(node, ast.FunctionDef):
                metadata['functions'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args]
                })
            
            # Extract class definitions
            elif isinstance(node, ast.ClassDef):
                metadata['classes'].append({
                    'name': node.name,
                    'line': node.lineno
                })
            
            # Extract imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    metadata['imports'].append({
                        'name': alias.name,
                        'asname': alias.asname,
                        'line': node.lineno
                    })
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    metadata['imports'].append({
                        'name': f"{module}.{alias.name}" if module else alias.name,
                        'asname': alias.asname,
                        'line': node.lineno,
                        'from': module
                    })
            
            # Extract variable assignments
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        metadata['variables'].append({
                            'name': target.id,
                            'line': node.lineno
                        })
        
        return metadata
    
    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific function
        
        Args:
            function_name: Name of the function
            
        Returns:
            Dictionary with function details or None
        """
        if not self.ast_tree:
            return None
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return {
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'decorators': [dec.id if isinstance(dec, ast.Name) else str(dec) 
                                  for dec in node.decorator_list],
                    'docstring': ast.get_docstring(node)
                }
        
        return None
    
    def get_complexity_score(self, code: str) -> int:
        """
        Calculate a simple complexity score based on code structure
        
        Args:
            code: Python code string
            
        Returns:
            Complexity score (higher = more complex)
        """
        try:
            tree = ast.parse(code)
            score = 0
            
            for node in ast.walk(tree):
                # Add complexity for control structures
                if isinstance(node, (ast.If, ast.While, ast.For)):
                    score += 1
                elif isinstance(node, ast.FunctionDef):
                    score += 2
                elif isinstance(node, ast.ClassDef):
                    score += 3
                elif isinstance(node, (ast.Try, ast.ExceptHandler)):
                    score += 1
            
            return score
        except:
            return 0
