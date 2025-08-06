#!/usr/bin/env python3
"""
Documentation Generator for Guinness App
Automatically generates and updates documentation
"""

import os
import ast
import datetime
from pathlib import Path
from typing import Dict, List, Set

class DocGenerator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.active_files = self.find_active_files()
        
    def find_active_files(self) -> Set[str]:
        """Find all Python files that are actively imported"""
        active = set()
        
        # Start with entry point
        entry_file = "guinness_app.py"
        active.add(entry_file)
        
        # Recursively find imports
        to_process = [entry_file]
        processed = set()
        
        while to_process:
            current = to_process.pop(0)
            if current in processed:
                continue
            processed.add(current)
            
            imports = self.get_imports(current)
            for imp in imports:
                if imp.endswith('.py') and os.path.exists(imp):
                    active.add(imp)
                    if imp not in processed:
                        to_process.append(imp)
        
        return active
    
    def get_imports(self, filename: str) -> List[str]:
        """Extract imports from a Python file"""
        imports = []
        try:
            with open(filename, 'r') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"{alias.name}.py")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(f"{node.module}.py")
        except:
            pass
        
        return imports
    
    def generate_structure_doc(self) -> str:
        """Generate project structure documentation"""
        doc = f"""# Project Structure Documentation
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

## Active Files

"""
        # Group files by category
        categories = {
            'Entry Point': ['guinness_app.py'],
            'Page Components': [],
            'Utilities': [],
            'Data/API': [],
            'UI Components': [],
            'Disabled Features': []
        }
        
        for file in sorted(self.active_files):
            if 'page' in file or 'report' in file:
                categories['Page Components'].append(file)
            elif 'utils' in file or 'helper' in file:
                categories['Utilities'].append(file)
            elif 'data' in file or 'api' in file or 'fetch' in file:
                categories['Data/API'].append(file)
            elif 'ui' in file or 'component' in file or 'logo' in file:
                categories['UI Components'].append(file)
            elif file not in categories['Entry Point']:
                categories['Utilities'].append(file)
        
        # Add disabled features
        disabled = ['bond_calculator_mockup.py', 'trade_calculator.py', 'ai_assistant.py']
        for file in disabled:
            if os.path.exists(file):
                categories['Disabled Features'].append(file)
        
        for category, files in categories.items():
            if files:
                doc += f"### {category}\n"
                for file in files:
                    doc += f"- `{file}`"
                    if file in disabled:
                        doc += " *(Currently disabled in navigation)*"
                    doc += "\n"
                doc += "\n"
        
        return doc
    
    def generate_api_doc(self) -> str:
        """Generate API documentation"""
        doc = """## API Documentation

### Main Navigation Functions

"""
        # Parse guinness_app.py for page functions
        with open('guinness_app.py', 'r') as f:
            content = f.read()
            
        # Extract function definitions
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.endswith('_page') or node.name.endswith('_report'):
                    doc += f"#### `{node.name}()`\n"
                    if ast.get_docstring(node):
                        doc += f"{ast.get_docstring(node)}\n"
                    doc += "\n"
        
        return doc
    
    def generate_full_documentation(self):
        """Generate complete documentation"""
        full_doc = self.generate_structure_doc()
        full_doc += self.generate_api_doc()
        
        # Add deployment info
        if os.path.exists('DEPLOYMENT_GUIDE.md'):
            full_doc += "\n## Deployment\n\nSee [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.\n"
        
        # Save documentation
        with open('DOCUMENTATION.md', 'w') as f:
            f.write(full_doc)
        
        print("Documentation generated: DOCUMENTATION.md")
        
        # Generate summary
        summary = f"""
Documentation Generated Successfully!

Active Files: {len(self.active_files)}
Total Python Files: {len(list(Path('.').glob('*.py')))}
Archived Files: {len(list(Path('.').glob('*.py'))) - len(self.active_files)}

See DOCUMENTATION.md for full details.
"""
        print(summary)
        
        return full_doc

if __name__ == "__main__":
    generator = DocGenerator()
    generator.generate_full_documentation()