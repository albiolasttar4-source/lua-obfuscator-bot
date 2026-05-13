import re
import random
import string
import base64
from typing import Dict, List, Tuple

class LuaObfuscator:
    """Advanced Lua code obfuscator with multiple techniques"""
    
    def __init__(self):
        self.var_map: Dict[str, str] = {}
        self.string_map: Dict[str, str] = {}
        self.function_map: Dict[str, str] = {}
        
    def generate_random_name(self, length: int = 8) -> str:
        """Generate random variable/function name"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def remove_comments_and_whitespace(self, code: str) -> str:
        """Remove comments and excessive whitespace"""
        # Remove single-line comments
        code = re.sub(r'--[^\n]*', '', code)
        
        # Remove multi-line comments
        code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
        
        # Remove excessive whitespace while preserving code structure
        lines = code.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        code = '\n'.join(lines)
        
        # Remove extra spaces around operators
        code = re.sub(r'\s*([=+\-*/%<>!]=?)\s*', r'\1', code)
        code = re.sub(r'\s*([,;(){}\[\]])\s*', r'\1', code)
        
        return code.strip()
    
    def randomize_variable_names(self, code: str) -> str:
        """Randomize variable and function names"""
        # Match variable assignments and function definitions
        var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        # Keywords that should not be obfuscated
        lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while', 'print', 'table',
            'string', 'math', 'os', 'io', 'require', 'error', 'assert'
        }
        
        def replace_var(match):
            var = match.group(1)
            if var in lua_keywords or var in self.var_map.values():
                return var
            
            if var not in self.var_map:
                self.var_map[var] = self.generate_random_name()
            
            return self.var_map[var]
        
        code = re.sub(var_pattern, replace_var, code)
        return code
    
    def encrypt_strings(self, code: str) -> str:
        """Encrypt string literals"""
        # Match string literals (both single and double quotes)
        string_pattern = r'(["\'])(?:(?=(\\?))\2.)*?\1'
        
        def encrypt_string(match):
            string_content = match.group(0)
            if string_content not in self.string_map:
                # Extract the actual string without quotes
                inner = string_content[1:-1]
                # Encode to base64
                encoded = base64.b64encode(inner.encode()).decode()
                # Store mapping
                self.string_map[string_content] = encoded
                # Return decryption code
                return f'(function()local _s="{encoded}";local _d="";for i=1,#_s,4 do _d=_d..string.char(tonumber(string.sub(_s,i,i+3)))end;return _d end)()'
            
            return self.string_map[string_content]
        
        code = re.sub(string_pattern, encrypt_string, code)
        return code
    
    def flatten_control_flow(self, code: str) -> str:
        """Add junk code and flatten control flow"""
        # Split code into lines
        lines = code.split('\n')
        obfuscated_lines = []
        
        for line in lines:
            obfuscated_lines.append(line)
            # Add junk code after certain lines
            if any(keyword in line for keyword in ['=', 'function', 'if', 'for', 'while']):
                junk = f"local _j{random.randint(1000, 9999)}={random.randint(1, 100)}"
                obfuscated_lines.append(junk)
        
        return '\n'.join(obfuscated_lines)
    
    def obfuscate(self, code: str) -> str:
        """Apply all obfuscation techniques"""
        # Reset maps for new code
        self.var_map = {}
        self.string_map = {}
        self.function_map = {}
        
        # Step 1: Remove comments and whitespace
        code = self.remove_comments_and_whitespace(code)
        
        # Step 2: Encrypt strings
        code = self.encrypt_strings(code)
        
        # Step 3: Randomize variable names
        code = self.randomize_variable_names(code)
        
        # Step 4: Flatten control flow
        code = self.flatten_control_flow(code)
        
        # Step 5: Final compression (remove unnecessary spaces)
        code = ' '.join(code.split())
        
        return code
