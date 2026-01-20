import ast
from typing import Dict, Any

class CodeParser:
    """
    Simple Python code parser
    """
    
    def parse_code(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code and return AST
        
        Args:
            code: String containing Python code
            
        Returns:
            Dictionary with parsing results
        """
        result = {
            'success': False,
            'ast': None,
            'error': None
        }
        
        try:
            result['ast'] = ast.parse(code)
            result['success'] = True
        except SyntaxError as e:
            result['error'] = f"Line {e.lineno}: {e.msg}"
        except Exception as e:
            result['error'] = str(e)
        
        return result
