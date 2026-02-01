#!/usr/bin/env python3
"""
Tool: Java Parser
Extracts Selenium patterns from Java source code using javalang.
Layer 3: Deterministic Tool
"""

import javalang
import json
from typing import Dict, List, Any


class JavaParser:
    """Parse Java source and extract Selenium/TestNG patterns."""
    
    SELENIUM_IMPORTS = [
        'org.openqa.selenium',
        'org.openqa.selenium.chrome',
        'org.openqa.selenium.firefox',
        'org.openqa.selenium.support',
        'org.openqa.selenium.support.ui',
        'org.openqa.selenium.interactions',
    ]
    
    TESTNG_ANNOTATIONS = ['Test', 'BeforeMethod', 'AfterMethod', 'BeforeClass', 'AfterClass', 'DataProvider']
    
    def __init__(self, source_code: str, file_name: str = ""):
        self.source_code = source_code
        self.file_name = file_name
        self.tree = None
        self.metadata = {
            'file_name': file_name,
            'class_name': '',
            'imports': [],
            'selenium_imports': [],
            'methods': [],
            'is_testng': False
        }
    
    def parse(self) -> Dict[str, Any]:
        """Parse Java source and return metadata."""
        try:
            self.tree = javalang.parse.parse(self.source_code)
        except javalang.parser.JavaSyntaxError as e:
            raise ValueError(f"Java syntax error: {e}")
        
        self._extract_imports()
        self._extract_classes()
        return self.metadata
    
    def _extract_imports(self):
        """Extract import statements."""
        for _, node in self.tree.filter(javalang.tree.Import):
            import_path = node.path
            self.metadata['imports'].append(import_path)
            
            # Check if it's a Selenium import
            for sel_import in self.SELENIUM_IMPORTS:
                if import_path.startswith(sel_import):
                    self.metadata['selenium_imports'].append(import_path)
            
            # Check if it's TestNG
            if 'org.testng' in import_path:
                self.metadata['is_testng'] = True
    
    def _extract_classes(self):
        """Extract class and method information."""
        for _, node in self.tree.filter(javalang.tree.ClassDeclaration):
            self.metadata['class_name'] = node.name
            
            for method in node.methods:
                method_info = self._extract_method(method)
                self.metadata['methods'].append(method_info)
    
    def _extract_method(self, method) -> Dict[str, Any]:
        """Extract method details including annotations and Selenium calls."""
        method_info = {
            'name': method.name,
            'annotations': [],
            'selenium_calls': [],
            'body': ''
        }
        
        # Extract annotations
        if method.annotations:
            for annotation in method.annotations:
                if isinstance(annotation, javalang.tree.Annotation):
                    name = annotation.name
                    if isinstance(name, list):
                        name = '.'.join(name)
                    method_info['annotations'].append(name)
        
        # Extract method body as string
        if method.body:
            for statement in method.body:
                self._extract_selenium_calls(statement, method_info['selenium_calls'])
        
        return method_info
    
    def _extract_selenium_calls(self, statement, calls_list: List[Dict]):
        """Recursively extract Selenium method invocations."""
        if statement is None:
            return
        
        # Skip non-node types
        if isinstance(statement, str):
            return
        
        # Check if this is a method invocation
        if isinstance(statement, javalang.tree.MethodInvocation):
            call_info = {
                'method': statement.member,
                'arguments': [],
                'qualifier': statement.qualifier
            }
            
            # Extract arguments
            if statement.arguments:
                for arg in statement.arguments:
                    call_info['arguments'].append(self._node_to_string(arg))
            
            calls_list.append(call_info)
            
            # Check for chained calls (e.g., driver.findElement().click())
            if statement.selectors:
                for selector in statement.selectors:
                    self._extract_selenium_calls(selector, calls_list)
        
        # Recursively check children
        if hasattr(statement, 'children'):
            for child in statement.children:
                if isinstance(child, list):
                    for item in child:
                        self._extract_selenium_calls(item, calls_list)
                elif isinstance(child, str):
                    continue
                elif child is not None:
                    self._extract_selenium_calls(child, calls_list)
    
    def _node_to_string(self, node) -> str:
        """Convert AST node to string representation."""
        if isinstance(node, javalang.tree.Literal):
            return node.value
        elif isinstance(node, javalang.tree.MemberReference):
            qualifier = f"{node.qualifier}." if node.qualifier else ""
            return f"{qualifier}{node.member}"
        elif isinstance(node, javalang.tree.BinaryOperation):
            left = self._node_to_string(node.operandl)
            right = self._node_to_string(node.operandr)
            return f"{left} {node.operator} {right}"
        else:
            return str(node)


def parse_java_file(file_path: str) -> Dict[str, Any]:
    """Parse a Java file and return metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    parser = JavaParser(source_code, file_path)
    return parser.parse()


def parse_java_source(source_code: str, file_name: str = "") -> Dict[str, Any]:
    """Parse Java source code and return metadata."""
    parser = JavaParser(source_code, file_name)
    return parser.parse()


if __name__ == '__main__':
    # Test with sample code
    sample = '''
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.Test;

public class LoginTest {
    private WebDriver driver;
    
    @Test
    public void testLogin() {
        driver.findElement(By.id("username")).sendKeys("admin");
        driver.findElement(By.id("password")).sendKeys("secret");
        driver.findElement(By.id("login")).click();
    }
}
'''
    
    result = parse_java_source(sample, "LoginTest.java")
    print(json.dumps(result, indent=2))
