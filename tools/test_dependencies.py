#!/usr/bin/env python3
"""
Test script to verify connectivity and dependencies for the converter.
Phase 2: Link (Connectivity)
"""

import sys

def test_javalang():
    """Test javalang library can parse Java code."""
    print("[TEST] Testing javalang library...")
    try:
        import javalang
        
        sample_java = """
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
"""
        tree = javalang.parse.parse(sample_java)
        
        # Count methods
        methods = list(tree.filter(javalang.tree.MethodDeclaration))
        print(f"  [OK] Parsed Java file successfully")
        print(f"  [INFO] Found {len(methods)} method(s)")
        
        # Check imports
        imports = list(tree.filter(javalang.tree.Import))
        print(f"  [INFO] Found {len(imports)} import(s)")
        
        return True
    except Exception as e:
        print(f"  [FAIL] javalang test failed: {e}")
        return False

def test_ollama():
    """Test Ollama connectivity with CodeLlama."""
    print("\n[TEST] Testing Ollama connectivity...")
    try:
        import ollama
        
        # Test connection by listing models
        models = ollama.list()
        print(f"  [OK] Ollama is running")
        print(f"  [INFO] Models response: {models}")
        
        # Test CodeLlama generation
        print("\n[TEST] Testing CodeLlama generation...")
        response = ollama.generate(
            model='codellama',
            prompt='Convert this Selenium Java to Playwright TypeScript:\n\ndriver.findElement(By.id("username")).sendKeys("admin");',
            options={'temperature': 0.1}
        )
        print(f"  [OK] CodeLlama response received")
        print(f"  [RESPONSE] {response['response'][:100]}...")
        return True
    except Exception as e:
        print(f"  [FAIL] Ollama test failed: {e}")
        print(f"  [HINT] Make sure Ollama is installed and running:")
        print(f"         1. Install Ollama: https://ollama.com")
        print(f"         2. Pull CodeLlama: ollama pull codellama")
        print(f"         3. Start Ollama: ollama serve")
        return False

def main():
    print("=" * 60)
    print("Phase 2: Link - Dependency Verification")
    print("=" * 60)
    
    results = []
    results.append(("javalang", test_javalang()))
    results.append(("ollama", test_ollama()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} - {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n[SUCCESS] All tests passed! Ready for Phase 3: Architect")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Please fix the issues before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
