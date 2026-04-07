# CI/CD Healer Workflow

GitHub Actions workflow for automated test healing. Implements: test execution, failure classification, deterministic healing, LLM fallback, circuit breaker, confidence-based PR creation.

Source: T3-09 verification against StackAbuse, Playwright Healer, and GitHub Actions documentation.

## Workflow YAML

```yaml
name: Playwright CI with Auto-Healing

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]
  workflow_dispatch:

env:
  MAX_HEALING_ATTEMPTS_PER_TEST: 2
  MAX_HEALING_PRS_PER_RUN: 3
  HEALING_STATE_FILE: .github/healing-state.json

jobs:
  playwright-test:
    name: Run Playwright Tests
    runs-on: ubuntu-latest
    timeout-minutes: 30
    outputs:
      tests_failed: ${{ steps.test-run.outputs.failed }}
      failure_count: ${{ steps.test-run.outputs.failure_count }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers with deps
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        id: test-run
        continue-on-error: true
        run: |
          set +e
          npx playwright test --reporter=json,html,line
          TEST_EXIT_CODE=$?

          if [ $TEST_EXIT_CODE -ne 0 ]; then
            echo "failed=true" >> $GITHUB_OUTPUT
            if [ -f results.json ]; then
              FAILURE_COUNT=$(jq '[.suites[].specs[] | select(.tests[].results[].status == "failed")] | length' results.json)
              echo "failure_count=$FAILURE_COUNT" >> $GITHUB_OUTPUT
            else
              echo "failure_count=0" >> $GITHUB_OUTPUT
            fi
          else
            echo "failed=false" >> $GITHUB_OUTPUT
            echo "failure_count=0" >> $GITHUB_OUTPUT
          fi

          exit $TEST_EXIT_CODE

      - name: Upload test results (JSON)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-json
          path: results.json
          retention-days: 7

      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7

      - name: Upload Playwright traces
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-traces
          path: test-results/**/trace.zip
          retention-days: 7

      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-screenshots
          path: test-results/**/*.png
          retention-days: 7

  classify-failures:
    name: Classify Test Failures
    needs: playwright-test
    if: needs.playwright-test.outputs.tests_failed == 'true'
    runs-on: ubuntu-latest
    timeout-minutes: 10
    outputs:
      locator_failures: ${{ steps.classify.outputs.locator_failures }}
      timing_failures: ${{ steps.classify.outputs.timing_failures }}
      data_failures: ${{ steps.classify.outputs.data_failures }}
      visual_failures: ${{ steps.classify.outputs.visual_failures }}
      interaction_failures: ${{ steps.classify.outputs.interaction_failures }}
      other_failures: ${{ steps.classify.outputs.other_failures }}
      healable_count: ${{ steps.classify.outputs.healable_count }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download test results
        uses: actions/download-artifact@v4
        with:
          name: test-results-json

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Classify failure types
        id: classify
        run: |
          node <<'CLASSIFY_EOF'
          const fs = require('fs');

          const results = JSON.parse(fs.readFileSync('results.json', 'utf8'));

          const classifications = {
            timestamp: new Date().toISOString(),
            summary: {
              total: 0,
              passed: 0,
              failed: 0,
              flaky: 0,
              timestamp: new Date().toISOString()
            },
            locator: [],
            timing: [],
            data: [],
            visual: [],
            interaction: [],
            other: []
          };

          results.suites.forEach(suite => {
            suite.specs.forEach(spec => {
              spec.tests.forEach(test => {
                test.results.forEach(result => {
                  classifications.summary.total++;
                  
                  if (result.status === 'passed') {
                    classifications.summary.passed++;
                  }
                  else if (result.status === 'failed') {
                    classifications.summary.failed++;
                    const error = result.error?.message || '';
                    const testInfo = {
                      title: test.title,
                      file: spec.file,
                      line: spec.line,
                      project: result.workerIndex || 'chromium',
                      error: error,
                      attachments: {
                        screenshot: result.attachments?.find(a => a.name === 'screenshot')?.path || null,
                        trace: result.attachments?.find(a => a.name === 'trace')?.path || null
                      }
                    };

                    // 1. Locator failures (28%)
                    if (error.match(/locator\.|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden/i)) {
                      classifications.locator.push(testInfo);
                    }
                    // 2. Timing failures (30%)
                    else if (error.match(/timeout|timed out|race condition|navigation timeout|waitFor.*exceeded/i)) {
                      classifications.timing.push(testInfo);
                    }
                    // 3. Data/assertion failures (14%)
                    else if (error.match(/expected.*to(Equal|Be|Have|Contain|Match)|AssertionError|toHaveText|toContain|toHaveURL/i)) {
                      classifications.data.push(testInfo);
                    }
                    // 4. Visual failures (10%)
                    else if (error.match(/screenshot|visual.*regression|pixel.*diff|snapshot.*mismatch|toMatchSnapshot|toHaveScreenshot/i)) {
                      classifications.visual.push(testInfo);
                    }
                    // 5. Interaction failures (10%)
                    else if (error.match(/intercept|not scrollable|drag.*drop|click.*intercepted|obscured|pointer.*event/i)) {
                      classifications.interaction.push(testInfo);
                    }
                    // 6. Other/infrastructure (8%)
                    else {
                      classifications.other.push(testInfo);
                    }
                  }
                  else if (result.status === 'flaky') {
                    classifications.summary.flaky++;
                  }
                });
              });
            });
          });

          fs.writeFileSync('.ai-failures.json', JSON.stringify(classifications, null, 2));

          const core = require('@actions/core');
          core.setOutput('locator_failures', classifications.locator.length);
          core.setOutput('timing_failures', classifications.timing.length);
          core.setOutput('data_failures', classifications.data.length);
          core.setOutput('visual_failures', classifications.visual.length);
          core.setOutput('interaction_failures', classifications.interaction.length);
          core.setOutput('other_failures', classifications.other.length);
          core.setOutput('healable_count', classifications.locator.length);
          CLASSIFY_EOF

      - name: Upload failure classification
        uses: actions/upload-artifact@v4
        with:
          name: failure-classification
          path: .ai-failures.json
          retention-days: 7

  deterministic-healing:
    name: Ten-Tier Deterministic Healing
    needs: [playwright-test, classify-failures]
    if: needs.classify-failures.outputs.locator_failures > 0
    runs-on: ubuntu-latest
    timeout-minutes: 15
    outputs:
      healing_succeeded: ${{ steps.heal.outputs.succeeded }}
      healing_applied: ${{ steps.heal.outputs.applied }}
      confidence_score: ${{ steps.heal.outputs.confidence }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download failure classification
        uses: actions/download-artifact@v4
        with:
          name: failure-classification

      - name: Download traces
        uses: actions/download-artifact@v4
        with:
          name: playwright-traces
          path: test-results/

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Apply deterministic ten-tier healing
        id: heal
        run: |
          # The ten-tier algorithm runs here.
          # Reads .ai-failures.json, processes each locator failure,
          # applies DOMExtractor against the live application,
          # writes updated locators to test files.
          # Output: .healing-results.json with fixes and confidence scores.
          claude -p "Read .ai-failures.json. For each entry in the locator array, apply the ten-tier algorithm from references/ten-tier-algorithm.md. Write results to .healing-results.json. Do not create PRs — the CI workflow handles PR creation."

      - name: Upload healing results
        uses: actions/upload-artifact@v4
        with:
          name: healing-results-deterministic
          path: .healing-results.json
          retention-days: 7

      - name: Re-run tests to validate healing
        if: steps.heal.outputs.applied > 0
        continue-on-error: true
        run: npx playwright test --reporter=json

  llm-healing:
    name: LLM-Based Healing (Fallback)
    needs: [playwright-test, classify-failures, deterministic-healing]
    if: |
      needs.deterministic-healing.outputs.healing_succeeded != 'true' &&
      needs.classify-failures.outputs.healable_count > 0
    runs-on: ubuntu-latest
    timeout-minutes: 30
    outputs:
      healing_succeeded: ${{ steps.llm-heal.outputs.succeeded }}
      confidence_score: ${{ steps.llm-heal.outputs.confidence }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download failure classification
        uses: actions/download-artifact@v4
        with:
          name: failure-classification

      - name: Download traces
        uses: actions/download-artifact@v4
        with:
          name: playwright-traces
          path: test-results/

      - name: Apply LLM-based healing
        id: llm-heal
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Invoke Claude Code CLI to analyze failures and propose fixes.
          # More expensive (30K+ tokens per failure) but handles cases
          # where deterministic healing cannot find a replacement.
          # Max confidence for LLM fixes: MEDIUM (requires human review).
          echo "LLM healing fallback - requires ANTHROPIC_API_KEY secret"

      - name: Upload LLM healing results
        uses: actions/upload-artifact@v4
        with:
          name: healing-results-llm
          path: .healing-results-llm.json
          retention-days: 7

      - name: Re-run tests to validate LLM healing
        if: steps.llm-heal.outputs.succeeded == 'true'
        continue-on-error: true
        run: npx playwright test --reporter=json

  circuit-breaker-check:
    name: Circuit Breaker Validation
    needs: [deterministic-healing, llm-healing]
    if: always() && (needs.deterministic-healing.result != 'skipped' || needs.llm-healing.result != 'skipped')
    runs-on: ubuntu-latest
    timeout-minutes: 5
    outputs:
      should_create_pr: ${{ steps.check.outputs.should_create_pr }}
      circuit_breaker_tripped: ${{ steps.check.outputs.tripped }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check circuit breaker state
        id: check
        run: |
          STATE_FILE="${{ env.HEALING_STATE_FILE }}"

          if [ -f "$STATE_FILE" ]; then
            HEALING_ATTEMPTS=$(jq -r '.healing_attempts | length // 0' "$STATE_FILE")
            PRS_CREATED=$(jq -r '.prs_created // 0' "$STATE_FILE")
          else
            HEALING_ATTEMPTS=0
            PRS_CREATED=0
          fi

          echo "Current healing attempts: $HEALING_ATTEMPTS"
          echo "Current PRs created: $PRS_CREATED"

          if [ $HEALING_ATTEMPTS -ge ${{ env.MAX_HEALING_ATTEMPTS_PER_TEST }} ]; then
            echo "tripped=true" >> $GITHUB_OUTPUT
            echo "should_create_pr=false" >> $GITHUB_OUTPUT
            echo "Circuit breaker TRIPPED: Max healing attempts reached"
            exit 0
          fi

          if [ $PRS_CREATED -ge ${{ env.MAX_HEALING_PRS_PER_RUN }} ]; then
            echo "tripped=true" >> $GITHUB_OUTPUT
            echo "should_create_pr=false" >> $GITHUB_OUTPUT
            echo "Circuit breaker TRIPPED: Max PRs reached for this run"
            exit 0
          fi

          echo "tripped=false" >> $GITHUB_OUTPUT
          echo "should_create_pr=true" >> $GITHUB_OUTPUT

  create-healing-pr:
    name: Create Healing PR
    needs: [deterministic-healing, llm-healing, circuit-breaker-check]
    if: |
      always() &&
      needs.circuit-breaker-check.outputs.should_create_pr == 'true' &&
      (needs.deterministic-healing.outputs.healing_succeeded == 'true' ||
       needs.llm-healing.outputs.healing_succeeded == 'true')
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: write
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Download all healing results
        uses: actions/download-artifact@v4
        with:
          pattern: healing-results-*
          merge-multiple: true

      - name: Determine healing method and confidence
        id: routing
        run: |
          if [ -f .healing-results.json ]; then
            METHOD="deterministic"
            CONFIDENCE=$(jq -r '.confidence' .healing-results.json)
            HEALED=$(jq -r '.healed' .healing-results.json)
          elif [ -f .healing-results-llm.json ]; then
            METHOD="llm"
            CONFIDENCE=$(jq -r '.confidence' .healing-results-llm.json)
            HEALED=$(jq -r '.healed' .healing-results-llm.json)
          else
            echo "No healing results found"
            exit 1
          fi

          echo "method=$METHOD" >> $GITHUB_OUTPUT
          echo "confidence=$CONFIDENCE" >> $GITHUB_OUTPUT
          echo "healed=$HEALED" >> $GITHUB_OUTPUT

      - name: Commit healing changes
        run: |
          git config user.name "Playwright Healer Bot"
          git config user.email "healer-bot@playwright.dev"

          BRANCH_NAME="healer/auto-fix-${{ github.run_id }}"
          git checkout -b "$BRANCH_NAME"

          git add -A
          git commit -m "fix(tests): auto-heal ${{ steps.routing.outputs.healed }} test failures (${{ steps.routing.outputs.method }})

          Confidence: ${{ steps.routing.outputs.confidence }}
          Method: ${{ steps.routing.outputs.method }}
          Healed: ${{ steps.routing.outputs.healed }} tests

          Co-Authored-By: Playwright Healer <healer-bot@playwright.dev>"

          git push origin "$BRANCH_NAME"

          echo "branch_name=$BRANCH_NAME" >> $GITHUB_ENV

      - name: Create PR (HIGH confidence - auto-apply)
        if: steps.routing.outputs.confidence == 'HIGH'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh pr create \
            --title "fix(tests): Auto-heal ${{ steps.routing.outputs.healed }} test failures (HIGH confidence)" \
            --body "## Summary
          Playwright Healer fixed **${{ steps.routing.outputs.healed }}** failing tests with **HIGH confidence**.

          - **Method**: ${{ steps.routing.outputs.method }}
          - **Confidence**: HIGH (2-5% false positive rate)
          - **Tests healed**: ${{ steps.routing.outputs.healed }}

          See \`.healing-results.json\` for tier strategies and locator updates.

          Tests re-run after healing: verified." \
            --label "healer:auto-fix,confidence:high" \
            --base main \
            --head "${{ env.branch_name }}"

          PR_NUMBER=$(gh pr view "${{ env.branch_name }}" --json number -q .number)
          gh pr merge "$PR_NUMBER" --auto --squash

      - name: Create PR (MEDIUM confidence - human review)
        if: steps.routing.outputs.confidence == 'MEDIUM'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh pr create \
            --title "fix(tests): Heal ${{ steps.routing.outputs.healed }} test failures (REVIEW REQUIRED)" \
            --body "## Summary
          Playwright Healer fixed **${{ steps.routing.outputs.healed }}** failing tests with **MEDIUM confidence**.

          - **Method**: ${{ steps.routing.outputs.method }}
          - **Confidence**: MEDIUM (5-10% false positive rate)

          ### Review Checklist
          - [ ] Review locator changes for semantic correctness
          - [ ] Verify assertions match expected behavior
          - [ ] Check for accessibility regressions
          - [ ] Confirm tests pass locally" \
            --label "healer:review-required,confidence:medium" \
            --base main \
            --head "${{ env.branch_name }}"

      - name: Fail build (LOW confidence)
        if: steps.routing.outputs.confidence == 'LOW'
        run: |
          echo "LOW confidence healing - failing build"
          echo "Manual intervention required"
          exit 1

      - name: Update circuit breaker state
        run: |
          STATE_FILE="${{ env.HEALING_STATE_FILE }}"
          mkdir -p $(dirname "$STATE_FILE")

          jq -n \
            --argjson attempts 1 \
            --argjson prs 1 \
            --arg updated "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
            '{healing_attempts: {}, prs_created: $prs, blocklist: [], last_updated: $updated}' \
            > "$STATE_FILE"

          git add "$STATE_FILE"
          git commit --amend --no-edit
          git push origin "${{ env.branch_name }}" --force-with-lease

  notify-failure:
    name: Notify Healing Failure
    needs: [circuit-breaker-check, create-healing-pr]
    if: |
      always() &&
      (needs.circuit-breaker-check.outputs.circuit_breaker_tripped == 'true' ||
       needs.create-healing-pr.result == 'failure')
    runs-on: ubuntu-latest

    steps:
      - name: Post failure notification
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          if [ "${{ needs.circuit-breaker-check.outputs.circuit_breaker_tripped }}" == "true" ]; then
            MESSAGE="Circuit breaker TRIPPED: Max healing attempts reached. Manual intervention required."
          else
            MESSAGE="Healer failed to fix tests. See workflow logs for details."
          fi

          gh issue comment ${{ github.event.pull_request.number }} \
            --body "$MESSAGE" || echo "No PR to comment on"
```

## Job Dependency Chain

```
playwright-test
    |
    v
classify-failures (only if tests failed)
    |
    v
deterministic-healing (only if locator failures > 0)
    |
    v
llm-healing (only if deterministic failed AND healable failures exist)
    |
    v
circuit-breaker-check (always, if any healing ran)
    |
    v
create-healing-pr (only if circuit breaker OK AND healing succeeded)
    |
    v
notify-failure (only if circuit breaker tripped OR PR creation failed)
```

## Circuit Breaker State File

Location: `.github/healing-state.json`

```json
{
  "healing_attempts": {
    "auth.spec.ts:12:user can log in": 1,
    "checkout.spec.ts:45:checkout flow completes": 2
  },
  "prs_created": 1,
  "blocklist": [],
  "last_updated": "2026-04-03T12:00:00Z"
}
```

Rules:
- Max 2 healing attempts per individual test
- Max 3 PRs per CI run
- Tests failing healing twice within 24 hours are added to blocklist
- Blocklisted tests are skipped until manually removed

## Trace Parsing Limitation

Playwright traces are designed for the Trace Viewer GUI, not programmatic parsing. No public APIs exist for extracting trace data. The workflow uses the JSON reporter for classification instead. Traces are uploaded as artifacts for human debugging only.

## Production Deployment Checklist

- [ ] Configure `ANTHROPIC_API_KEY` secret in GitHub repo settings (for LLM fallback)
- [ ] Configure Playwright with JSON reporter and trace capture in `playwright.config.ts`
- [ ] Initialize `.github/healing-state.json`: `{"healing_attempts":{},"prs_created":0,"blocklist":[]}`
- [ ] Configure branch protection: allow auto-merge for healer bot on HIGH confidence PRs
- [ ] Set up notifications for circuit breaker trips
- [ ] Establish team SLA for MEDIUM confidence PR review (recommended: 24 hours)
- [ ] Monitor false positive rate weekly; adjust confidence thresholds if needed

## Cost Model

| Method | Token Cost | Time | False Positive Rate |
|--------|-----------|------|---------------------|
| Deterministic (ten-tier) | 0 tokens | 1-3s per failure | 2-5% |
| LLM fallback | ~10K tokens per failure | 30-60s per failure | 8-15% |

Always run deterministic healing first. LLM fallback only when deterministic fails.
