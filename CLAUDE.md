Run sheet for this folder: `PLAN.md`. Phase 0 (text extraction and page rendering) is already done; `work/text/` and `work/pages/` exist and stay as they are.
Verification gate: `tools/check_all.sh work`, which prints one PASS or FAIL line. After editing anything in `tools/`, run `tools/test_checks.sh`.

## Agent skills

### Issue tracker

Issues and specs live as markdown files under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, each label string equal to its name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the root, created lazily. See `docs/agents/domain.md`.
