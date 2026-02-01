# SOP: Java AST Parsing

## Goal
Parse Selenium Java source code into an Abstract Syntax Tree (AST) to extract:
- Import statements (Selenium/TestNG dependencies)
- Class and method declarations
- Annotations (@Test, @BeforeMethod, @FindBy, etc.)
- Method invocations (Selenium API calls)
- Variable declarations

## Input
- Java source code as string
- File name for context

## Output
- Parsed AST nodes
- Extracted metadata dictionary

## Tool Logic

### Step 1: Parse Java Source
```python
import javalang

tree = javalang.parse.parse(java_source_code)
```

### Step 2: Extract Imports
```python
imports = []
for _, node in tree.filter(javalang.tree.Import):
    imports.append(node.path)
```

### Step 3: Extract Class Info
```python
for _, node in tree.filter(javalang.tree.ClassDeclaration):
    class_name = node.name
    methods = [m for m in node.methods]
```

### Step 4: Extract Selenium Elements
```python
selenium_patterns = {
    'findElement': 'locator',
    'sendKeys': 'fill',
    'click': 'click',
    'getText': 'textContent',
    # ... more mappings
}
```

## Edge Cases
1. **Syntax errors** in Java source → Return error with line number
2. **Nested classes** → Flatten or preserve hierarchy based on context
3. **Anonymous classes** → Skip or log for manual review
4. **Generic types** → Strip generics for simpler processing

## Data Schema (Output)
```json
{
  "file_name": "string",
  "class_name": "string",
  "imports": ["string"],
  "methods": [
    {
      "name": "string",
      "annotations": ["string"],
      "selenium_calls": [
        {
          "method": "string",
          "arguments": ["string"],
          "line_number": "number"
        }
      ]
    }
  ]
}
```
