# Findings Log: Selenium Java to Playwright TypeScript Converter

## Research & Discoveries

### Discovery Phase Answers (Phase 1)
**Date**: 2026-02-02

| Question | Answer |
|----------|--------|
| **North Star** | Enable QA teams to migrate Selenium tests to Playwright in JS/TS |
| **Integrations** | Local LLM (Ollama **CodeLlama**) for intelligent conversion |
| **Source of Truth** | UI input - user provides Selenium Java code |
| **Delivery Payload** | Converted code → new directory + display in UI |
| **Behavioral Rules** | **Convert Everything** - comprehensive, best-effort conversion |

### Key Insights
- **Target Framework**: TestNG (primary), JUnit patterns also relevant
- **LLM Integration**: Ollama **CodeLlama** for code generation
- **Dual Output**: Filesystem + UI display
- **Language Options**: Both JavaScript and TypeScript support

---

### Research Results (Phase 1)

#### Java AST Parsing Libraries
**Primary Recommendation: `javalang`**
- Pure Python library (no JVM dependency!)
- GitHub: https://github.com/c2nes/javalang
- Supports Java 8 syntax
- Can parse Java source code and extract:
  - Class definitions
  - Method declarations
  - Annotations (@Test, @FindBy, etc.)
  - Import statements
  - Method invocations (Selenium API calls)

**Alternative: JavaParser**
- Java-based library (requires JVM)
- More mature but heavier dependency

#### Ollama Integration
**Two approaches:**
1. **Python `ollama` library**: `pip install ollama`
   ```python
   from ollama import generate
   response = generate('codellama', prompt)  # or 'codellama:7b', 'codellama:13b'
   ```
2. **REST API**: Direct HTTP calls to `http://localhost:11434`

**Key Points:**
- Ollama runs locally on port 11434 by default
- Streaming endpoint available
- Model: **CodeLlama** (optimized for code generation)

#### Selenium → Playwright Migration Resources
Found excellent migration guides:
1. **BrowserStack Guide**: Structured migration approach
2. **Allegro Tech Blog**: Java-specific migration patterns
3. **MuukTest**: Command mapping between frameworks

**Key Mappings Identified:**
| Selenium (Java) | Playwright (JS/TS) |
|-----------------|-------------------|
| `driver.findElement(By.id())` | `page.locator()` |
| `sendKeys()` | `fill()` |
| `click()` | `click()` |
| `WebDriverWait` | `expect().toPass()` or auto-waiting |
| `@FindBy` | Direct locators or Page Object pattern |
| `Actions` class | Playwright's built-in actions |

### To Be Researched (Phase 1 Continued)
- [x] Java AST parsing libraries (JavaParser, javalang, etc.)
- [x] Ollama API integration patterns
- [x] Selenium to Playwright migration guides
- [ ] Existing open-source converters on GitHub
- [ ] Two-pane UI libraries for code comparison
- [ ] TestNG annotations mapping to Playwright Test

---

## Constraints Identified

### Technical Constraints
- Must handle Java syntax variations (different Selenium styles)
- TypeScript output must be valid and follow Playwright best practices
- Need to preserve test logic semantics during conversion
- Ollama llama 3.2 must be installed locally
- Support both JS and TS output based on user preference

### Business Constraints
- QA teams may have varying Java/Selenium coding styles
- Must handle partial/incomplete conversions gracefully
- UI must be intuitive for non-technical QA users

---

## Known Challenges
1. **Selenium API Mapping**: Selenium has multiple ways to do the same thing (findElement, @FindBy, PageFactory, etc.)
2. **Java-to-TS Type Mapping**: Need to map Java types to TypeScript types appropriately
3. **Async/Await**: Playwright is async; need to inject async/await patterns
4. **Assertions**: Different assertion libraries (JUnit/TestNG vs Playwright assertions)

---

## Resources Found
*To be populated during Phase 1 research*

---

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| | | |
