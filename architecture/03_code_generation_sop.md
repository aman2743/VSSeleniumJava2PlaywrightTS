# SOP: Playwright Code Generation

## Goal
Generate valid, idiomatic Playwright JavaScript/TypeScript code from parsed Selenium Java AST.

## Input
- Parsed AST metadata
- Target language (javascript | typescript)
- Mapping decisions from SOP 02

## Output
- Complete Playwright test file content
- File name with proper extension

## Tool Logic

### Step 1: Generate Imports
```typescript
// TypeScript
import { test, expect } from '@playwright/test';

// JavaScript
const { test, expect } = require('@playwright/test');
```

### Step 2: Generate Test Structure
```typescript
test.describe('ClassName', () => {
  test.beforeEach(async ({ page }) => {
    // Setup code
  });

  test('methodName', async ({ page }) => {
    // Test code
  });
});
```

### Step 3: Convert Selenium Calls
```typescript
// Java
 driver.findElement(By.id("username")).sendKeys("admin");

// TypeScript
await page.locator('#username').fill('admin');
```

### Step 4: Add Proper Async/Await
All Playwright operations return Promises:
```typescript
// Correct
await page.goto('https://example.com');
await page.locator('#btn').click();

// Incorrect (missing await)
page.goto('https://example.com');
```

## Code Templates

### TypeScript Template
```typescript
import { test, expect } from '@playwright/test';

test.describe('{{class_name}}', () => {
{{before_each}}
{{tests}}
});
```

### JavaScript Template
```javascript
const { test, expect } = require('@playwright/test');

test.describe('{{class_name}}', () => {
{{before_each}}
{{tests}}
});
```

## Edge Cases
1. **Missing mappings** → Add comment: `// TODO: Manual conversion needed`
2. **Complex expressions** → Use LLM for semantic conversion
3. **Custom utilities** → Import as-is, flag for review
4. **Data providers** → Convert to `test.each()` pattern

## Quality Checks
1. Valid syntax (parse with TypeScript compiler)
2. Proper indentation
3. Consistent quote style (single preferred)
4. All `await` keywords present
