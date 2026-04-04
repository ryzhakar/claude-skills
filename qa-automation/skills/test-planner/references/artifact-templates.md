# Artifact Templates

Output format templates for test-planner skill artifacts.

## Project Configuration Template

```markdown
# Project Configuration

**Framework:** React 18 / Next.js 14
**State Management:** Zustand
**Auth:** NextAuth.js (session-based)
**Build Tool:** Vite
**Base URL:** http://localhost:3000
**Detected:** {YYYY-MM-DD}
```

For Leptos, Yew, or other WASM frameworks, add:

```markdown
**Wait Strategy:** domcontentloaded + 150ms hydration buffer (WASM)
```

## Verification Evidence Template

```markdown
# Verification Evidence

## Pages Visited
- /login -- form with 2 labeled inputs (Email, Password), 1 submit button
- /dashboard -- 3 KPI widgets (dynamic), navigation sidebar, user avatar
- /products -- product grid with 12 items, search input, pagination

## Interactions Tested
- Login form: fill Email + Password -> click Sign In -> redirects to /dashboard
- Product search: type in search input -> grid filters in real time
- Cart: click "Add to Cart" -> cart badge increments from 0 to 1

## Issues Found
- /dashboard KPI widgets lack ARIA labels (need data-testid)
- /products list uses list-style: none (Safari list role issue per locator-strategy.md)

## Screenshots
- /tmp/login-page.png
- /tmp/dashboard-loaded.png
```

## Page Inventory Template

```markdown
# Page Inventory

- [x] /login (Score: 95)
  - Email input: labeled, getByLabel works
  - Password input: labeled, getByLabel works
  - Submit button: native button, getByRole works
  - Verdict: semantic locators sufficient

- [x] /dashboard (Score: 65)
  - User widget: div-based, no ARIA label (needs data-testid)
  - Navigation: semantic <nav>, getByRole works
  - KPI cards: dynamic content, no test IDs (needs data-testid)
  - Verdict: mixed quality, flag elements needing test IDs

- [ ] /settings -- not yet explored
```

## Selector Strategy Template

```markdown
# Selector Strategy

## Page: /login (Score: 95)
**Approach:** Semantic locators only
- Email input: getByLabel('Email')
- Password input: getByLabel('Password')
- Submit button: getByRole('button', { name: 'Sign In' })

## Page: /dashboard (Score: 65)
**Approach:** Mixed -- semantic where available, test IDs for dynamic elements
- User widget: getByTestId('user-widget') -- no ARIA label
- Navigation menu: getByRole('navigation') -- semantic landmark present
- KPI cards: getByTestId('kpi-card-revenue') -- dynamic content, no stable text

**Needed Test IDs (flag for dev team):**
- User widget wrapper
- Individual KPI cards
- Notification bell icon
```

## Test Plan Template

```markdown
# Test Plan: {Feature Name}

**Date:** {YYYY-MM-DD}
**Feature:** {Description from user request}
**Coverage Goal:** {Critical paths / Full coverage / Smoke tests}
**Base URL:** {URL from Phase 1}

---

## Scenario 1: {Name}

**Priority:** P0 (Critical)
**Preconditions:** Logged in as standard user
**Steps:**
1. Navigate to /products
2. Click "Add to Cart" on first product
3. Open cart overlay
4. Click "Checkout"

**Expected Outcomes:**
- Cart overlay shows product name, price, quantity matching the product clicked
- Checkout page loads with cart summary
- Product quantity persists across page navigation

**Edge Cases:**
- Cart is empty -> empty state message visible
- Product out of stock -> "Add to Cart" button disabled

**Test Suite:** checkout.spec.ts
**Dependencies:** Auth fixture, product catalog data

---

## Test Coverage Summary

| Feature | Suite | Tests | Priority | Status |
|---------|-------|-------|----------|--------|
| Authentication | auth.spec.ts | 8 | P0 | [ ] |
| Product Browsing | product.spec.ts | 10 | P1 | [ ] |
| Checkout | checkout.spec.ts | 12 | P0 | [ ] |
```
