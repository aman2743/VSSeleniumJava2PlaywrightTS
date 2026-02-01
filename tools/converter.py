#!/usr/bin/env python3
"""
Tool: Main Converter (Orchestrator)
Coordinates parsing and conversion.
Layer 3: Deterministic Tool
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

from tools.java_parser import parse_java_source
from tools.llm_converter import LLMConverter


class SeleniumToPlaywrightConverter:
    """
    Main converter orchestrator.
    Converts Selenium Java test files to Playwright JS/TS.
    """
    
    def __init__(self, target_language: str = 'typescript', output_dir: str = 'output'):
        self.target_language = target_language
        self.output_dir = output_dir
        self.extension = '.spec.ts' if target_language == 'typescript' else '.spec.js'
        self.converter = LLMConverter(target_language)
    
    def convert(self, java_source: str, file_name: str = '') -> Dict[str, Any]:
        """
        Convert Java source code to Playwright.
        
        Args:
            java_source: Java source code string
            file_name: Original file name for context
        
        Returns:
            Dictionary with conversion results
        """
        # Step 1: Parse Java source
        try:
            metadata = parse_java_source(java_source, file_name)
        except ValueError as e:
            return {
                'success': False,
                'error': f'Parse error: {e}',
                'original_code': java_source,
                'converted_code': '',
                'output_file': ''
            }
        
        # Step 2: Convert using LLM
        try:
            converted_code = self.converter.convert_with_context(java_source, metadata)
        except RuntimeError as e:
            return {
                'success': False,
                'error': f'Conversion error: {e}',
                'original_code': java_source,
                'converted_code': '',
                'output_file': ''
            }
        
        # Step 3: Prepare output file name
        if file_name:
            base_name = Path(file_name).stem
            # Convert CamelCase to kebab-case
            output_name = self._camel_to_kebab(base_name) + self.extension
        else:
            output_name = 'converted' + self.extension
        
        output_path = os.path.join(self.output_dir, output_name)
        
        # Step 4: Save to file
        os.makedirs(self.output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_code)
        
        return {
            'success': True,
            'error': None,
            'original_code': java_source,
            'converted_code': converted_code,
            'output_file': output_path,
            'metadata': metadata
        }
    
    def convert_file(self, file_path: str) -> Dict[str, Any]:
        """
        Convert a Java file to Playwright.
        
        Args:
            file_path: Path to Java file
        
        Returns:
            Dictionary with conversion results
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            java_source = f.read()
        
        return self.convert(java_source, file_path)
    
    def _camel_to_kebab(self, name: str) -> str:
        """Convert CamelCase to kebab-case."""
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('-')
            result.append(char.lower())
        return ''.join(result)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert Selenium Java tests to Playwright JS/TS'
    )
    parser.add_argument(
        'input',
        help='Java source file or directory'
    )
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Output directory (default: output)'
    )
    parser.add_argument(
        '-l', '--language',
        choices=['javascript', 'typescript'],
        default='typescript',
        help='Target language (default: typescript)'
    )
    
    args = parser.parse_args()
    
    converter = SeleniumToPlaywrightConverter(
        target_language=args.language,
        output_dir=args.output
    )
    
    if os.path.isfile(args.input):
        print(f"Converting: {args.input}")
        result = converter.convert_file(args.input)
        
        if result['success']:
            print(f"Success! Output: {result['output_file']}")
        else:
            print(f"Error: {result['error']}")
    
    elif os.path.isdir(args.input):
        java_files = list(Path(args.input).glob('**/*.java'))
        print(f"Found {len(java_files)} Java files")
        
        for java_file in java_files:
            print(f"Converting: {java_file}")
            result = converter.convert_file(str(java_file))
            
            if result['success']:
                print(f"  -> {result['output_file']}")
            else:
                print(f"  Error: {result['error']}")
    
    else:
        print(f"Error: {args.input} is not a valid file or directory")


if __name__ == '__main__':
    main()
