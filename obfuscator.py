import re
import random
import string
import base64
from typing import Dict, List, Tuple

class LuaObfuscator:
    """Advanced Lua code obfuscator with multiple levels"""
    
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
    
    def add_junk_code_heavy(self, code: str) -> str:
        """Add heavy junk code for maximum obfuscation"""
        lines = code.split('\n')
        obfuscated_lines = []
        
        for i, line in enumerate(lines):
            # Add multiple junk lines
            for _ in range(random.randint(2, 5)):
                junk = f"local _x{random.randint(10000, 99999)}=math.random({random.randint(1, 1000)})"
                obfuscated_lines.append(junk)
            
            obfuscated_lines.append(line)
            
            # Add more junk after important lines
            if any(keyword in line for keyword in ['print', 'return', 'function']):
                for _ in range(random.randint(1, 3)):
                    junk = f"local _y{random.randint(10000, 99999)}={random.randint(1, 100)}*{random.randint(1, 100)}"
                    obfuscated_lines.append(junk)
        
        return '\n'.join(obfuscated_lines)
    
    def obfuscate(self, code: str, level: int = 1) -> str:
        """
        Apply obfuscation techniques based on level:
        Level 1 (Normal): Basic obfuscation
        Level 2 (Medium): Advanced obfuscation
        Level 3 (Max): Maximum obfuscation
        """
        # Reset maps for new code
        self.var_map = {}
        self.string_map = {}
        self.function_map = {}
        
        if level == 1:
            # Level 1: Basic obfuscation
            code = self.remove_comments_and_whitespace(code)
            code = self.randomize_variable_names(code)
        
        elif level == 2:
            # Level 2: Medium obfuscation
            code = self.remove_comments_and_whitespace(code)
            code = self.encrypt_strings(code)
            code = self.randomize_variable_names(code)
        
        elif level == 3:
            # Level 3: Maximum obfuscation
            code = self.remove_comments_and_whitespace(code)
            code = self.encrypt_strings(code)
            code = self.randomize_variable_names(code)
            code = self.flatten_control_flow(code)
            code = self.add_junk_code_heavy(code)
        
        # Final compression (remove unnecessary spaces)
        code = ' '.join(code.split())
        
        return code
