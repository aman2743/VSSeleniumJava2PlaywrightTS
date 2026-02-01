#!/usr/bin/env python3
"""
Tool: LLM Converter
Uses Ollama CodeLlama for intelligent code conversion.
Layer 3: Deterministic Tool
"""

import ollama
from typing import Dict, Any


class LLMConverter:
    """Convert Selenium Java to Playwright JS/TS using CodeLlama."""
    
    MODEL = 'codellama'
    
    SYSTEM_PROMPT = """You are an expert in test automation migration.
Convert Selenium Java code to Playwright TypeScript/JavaScript.

Rules:
1. Convert Selenium API calls to Playwright equivalents
2. Use proper async/await syntax
3. Replace TestNG assertions with Playwright expect
4. Use Playwright's locator API
5. Return ONLY the converted code, no explanations
6. Ensure the output is valid, runnable TypeScript/JavaScript

Selenium to Playwright mappings:
- driver.findElement(By.id("x")) -> page.locator('#x')
- sendKeys("text") -> fill('text')
- click() -> click()
- getText() -> textContent()
- driver.get("url") -> page.goto('url')
- Thread.sleep(ms) -> page.waitForTimeout(ms)
- @Test -> test('name', async () => {...})
- Assert.assertEquals(a,b) -> expect(a).toBe(b)
"""

    def __init__(self, target_language: str = 'typescript'):
        self.target_language = target_language
        self.extension = '.ts' if target_language == 'typescript' else '.js'
    
    def convert(self, java_code: str, class_name: str = '') -> str:
        """
        Convert Java code to Playwright using LLM.
        
        Args:
            java_code: The Java source code to convert
            class_name: Optional class name for context
        
        Returns:
            Converted Playwright code
        """
        lang = 'TypeScript' if self.target_language == 'typescript' else 'JavaScript'
        
        prompt = f"""Convert this Selenium Java code to Playwright {lang}.

Original Java code:
```java
{java_code}
```

Provide ONLY the converted Playwright {lang} code. No explanations.

Requirements:
- Use @playwright/test
- Include proper imports
- Use async/await
- Convert all Selenium calls to Playwright equivalents
- Replace TestNG annotations with Playwright test structure
"""
        
        try:
            response = ollama.generate(
                model=self.MODEL,
                prompt=prompt,
                system=self.SYSTEM_PROMPT,
                options={
                    'temperature': 0.1,
                    'num_predict': 2048
                }
            )
            
            converted_code = response['response'].strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if converted_code.startswith('```'):
                lines = converted_code.split('\n')
                # Remove first line (```typescript or ```javascript)
                if lines[0].startswith('```'):
                    lines = lines[1:]
                # Remove last line (```)
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                converted_code = '\n'.join(lines).strip()
            
            return converted_code
            
        except Exception as e:
            raise RuntimeError(f"LLM conversion failed: {e}")
    
    def convert_with_context(self, java_code: str, metadata: Dict[str, Any]) -> str:
        """
        Convert with additional context from parser.
        
        Args:
            java_code: The Java source code
            metadata: Parsed metadata from JavaParser
        
        Returns:
            Converted Playwright code
        """
        class_name = metadata.get('class_name', 'ConvertedTest')
        return self.convert(java_code, class_name)


def convert_code(java_code: str, target_language: str = 'typescript') -> str:
    """Convenience function to convert code."""
    converter = LLMConverter(target_language)
    return converter.convert(java_code)


if __name__ == '__main__':
    # Test conversion
    sample_java = '''
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.Test;
import static org.testng.Assert.assertEquals;

public class LoginTest {
    private WebDriver driver;
    
    @Test
    public void testLogin() {
        driver.get("https://example.com/login");
        driver.findElement(By.id("username")).sendKeys("admin");
        driver.findElement(By.id("password")).sendKeys("secret");
        driver.findElement(By.id("login")).click();
        String welcomeText = driver.findElement(By.id("welcome")).getText();
        assertEquals(welcomeText, "Welcome, admin!");
    }
}
'''
    
    print("Converting to TypeScript...")
    converter = LLMConverter('typescript')
    result = converter.convert(sample_java)
    print("\n--- Converted Code ---")
    print(result)
