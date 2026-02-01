# SOP: Selenium to Playwright Mapping

## Goal
Map Selenium Java API calls to their Playwright JavaScript/TypeScript equivalents.

## Mapping Reference

### Locators
| Selenium (Java) | Playwright (JS/TS) |
|-----------------|-------------------|
| `By.id("value")` | `page.locator('#value')` |
| `By.name("value")` | `page.locator('[name="value"]')` |
| `By.className("value")` | `page.locator('.value')` |
| `By.cssSelector("value")` | `page.locator('value')` |
| `By.xpath("value")` | `page.locator('xpath=value')` |
| `By.linkText("value")` | `page.getByText('value')` |
| `By.partialLinkText("value")` | `page.getByText('value', {exact: false})` |
| `By.tagName("value")` | `page.locator('value')` |

### Actions
| Selenium (Java) | Playwright (JS/TS) |
|-----------------|-------------------|
| `element.sendKeys("text")` | `element.fill('text')` |
| `element.click()` | `element.click()` |
| `element.clear()` | `element.fill('')` or `element.clear()` |
| `element.submit()` | `element.press('Enter')` |
| `element.getText()` | `element.textContent()` |
| `element.getAttribute("attr")` | `element.getAttribute('attr')` |
| `element.isDisplayed()` | `element.isVisible()` |
| `element.isEnabled()` | `element.isEnabled()` |
| `element.isSelected()` | `element.isChecked()` |

### Navigation
| Selenium (Java) | Playwright (JS/TS) |
|-----------------|-------------------|
| `driver.get("url")` | `await page.goto('url')` |
| `driver.navigate().to("url")` | `await page.goto('url')` |
| `driver.navigate().back()` | `await page.goBack()` |
| `driver.navigate().forward()` | `await page.goForward()` |
| `driver.navigate().refresh()` | `await page.reload()` |
| `driver.getCurrentUrl()` | `page.url()` |
| `driver.getTitle()` | `await page.title()` |

### Waits
| Selenium (Java) | Playwright (JS/TS) |
|-----------------|-------------------|
| `Thread.sleep(ms)` | `await page.waitForTimeout(ms)` |
| `WebDriverWait + ExpectedConditions` | Playwright has auto-waiting |
| `wait.until(ExpectedConditions...)` | Use assertions with expect |

### TestNG to Playwright Test
| TestNG (Java) | Playwright Test (JS/TS) |
|---------------|-------------------------|
| `@Test` | `test('description', async () => { ... })` |
| `@BeforeMethod` | `test.beforeEach(async () => { ... })` |
| `@AfterMethod` | `test.afterEach(async () => { ... })` |
| `@BeforeClass` | `test.beforeAll(async () => { ... })` |
| `@AfterClass` | `test.afterAll(async () => { ... })` |
| `Assert.assertEquals(a, b)` | `expect(a).toBe(b)` |
| `Assert.assertTrue(cond)` | `expect(cond).toBeTruthy()` |
| `Assert.assertFalse(cond)` | `expect(cond).toBeFalsy()` |
| `Assert.assertNull(obj)` | `expect(obj).toBeNull()` |
| `Assert.assertNotNull(obj)` | `expect(obj).not.toBeNull()` |

## Tool Logic
1. Detect Selenium API method from AST
2. Look up equivalent Playwright API
3. Transform arguments (By.xxx → selector string)
4. Add `await` for async operations
5. Wrap in proper test structure

## Edge Cases
1. **Chain calls**: `driver.findElement().findElement()` → nested locators
2. **Actions class**: Complex mouse/keyboard → Playwright's locator actions
3. **Select class**: Dropdown handling → `page.selectOption()`
4. **Alert handling**: `driver.switchTo().alert()` → `page.on('dialog')`
5. **Frames**: `driver.switchTo().frame()` → `page.frameLocator()`
6. **Multiple windows**: `driver.getWindowHandles()` → `context.pages()`
