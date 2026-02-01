# Project Constitution: Selenium Java to Playwright TypeScript Converter

## Identity
**Project**: Selenium Java → Playwright TypeScript Converter  
**Pilot**: System Agent  
**Protocol**: B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger)  
**Status**: Phase 0 - Initialization

---

## Data Schemas

### Discovery Answers Summary
- **North Star**: Enable QA teams to migrate Selenium tests to Playwright in JS/TS
- **Integrations**: Local LLM (Ollama llama 3.2) for intelligent conversion
- **Source of Truth**: UI input - user provides Selenium Java code
- **Delivery Payload**: Converted code → new directory + display in UI
- **Behavioral Rules**: Convert Everything (best-effort, comprehensive)

### Input Schema (Selenium Java + TestNG Code)
```json
{
  "type": "selenium_testng_java_source",
  "version": "1.0",
  "properties": {
    "source_code": "string - Java source file content",
    "file_name": "string - original filename (e.g., LoginTest.java)",
    "test_framework": "string - TestNG (primary), JUnit (secondary)",
    "selenium_patterns": ["WebDriver", "PageFactory", "@FindBy", "Actions", "Waits"]
  }
}
```

### Processing Schema (LLM-Augmented)
```json
{
  "type": "conversion_request",
  "version": "1.0",
  "properties": {
    "java_ast": "object - parsed Java AST representation",
    "selenium_elements": "array - detected Selenium API calls",
    "llm_prompt": "string - structured prompt for Ollama CodeLlama",
    "target_language": "enum - 'javascript' | 'typescript'",
  }
}
```

### Output Schema (Playwright JS/TS Code)
```json
{
  "type": "playwright_js_ts_source",
  "version": "1.0",
  "properties": {
    "source_code": "string - Generated JS/TS file content",
    "file_name": "string - target filename (e.g., login.spec.ts)",
    "output_directory": "string - path to output directory",
    "conversion_log": "array - mapping of Selenium→Playwright patterns used",
    "confidence_score": "number - LLM confidence in conversion"
  }
}
```

### UI Delivery Schema
```json
{
  "type": "ui_payload",
  "version": "1.0",
  "properties": {
    "original_code": "string - Java source for side-by-side view",
    "converted_code": "string - Playwright output",
    "download_path": "string - path to generated file",
    "warnings": "array - any non-convertible patterns flagged",
    "success": "boolean - conversion status"
  }
}
```

---

## Behavioral Rules

### Conversion Rules
1. **Preserve Logic**: All test logic must be preserved semantically
2. **Playwright Idioms**: Output should follow Playwright best practices
3. **Type Safety**: Generated TypeScript must be type-safe
4. **Comments**: Preserve meaningful comments from source

### Do Not Rules
1. Do not execute generated code without user review
2. Do not assume business logic intent - convert literally
3. Do not skip validation of output syntax

---

## Architectural Invariants

### 3-Layer Architecture
1. **Layer 1 (Architecture)**: Markdown SOPs in `architecture/`
2. **Layer 2 (Navigation)**: Routing and orchestration logic
3. **Layer 3 (Tools)**: Atomic Python scripts in `tools/`

### Data Flow
```
Java Source → Parser → AST → Mapper → Generator → TypeScript Output
```

---

## Maintenance Log

| Date | Change | Author |
|------|--------|--------|
| 2026-02-02 | Initial constitution created | System Pilot |

---

## Pending Definitions
- [ ] Exact Selenium API coverage scope
- [ ] TypeScript target version
- [ ] Handling of external dependencies (Page Objects, utilities)
- [ ] Test framework mapping (JUnit/TestNG → Playwright Test)
