# Automatic PR review and feedback loop

## What can be triggered

Codex GitHub Code Review is a separate task using PR context and applicable AGENTS guidance. It does not resume this particular chat or carry its hidden conversation state. Put the relevant context in the repository, PR and evidence manifest.

Official documentation checked 2026-11-04: https://learn.chatgpt.com/docs/third-party/github . Connect the repository, enable Automatic review in repository settings and personal preferences, and select the available review trigger. For an explicit request post `@codex review`. A follow-up such as `@codex fix the P1 issue` can start a cloud task with branch-write permission. Native review concentrates on serious issues and does not replace engineering validation, CI or product acceptance.

Recommended first deployment: native automatic review plus existing GitHub CI. Manager watches PR review/check status and continues independent tasks. Do not add a paid API runner or webhook service until this path has been verified. An API/CLI runner would need its own credentials, budget, untrusted-code isolation, retry/idempotency and operational ownership.

## Setup and verification

1. In Codex code-review settings enable Quantic-Studio and appropriate author/event coverage. Check bot-authored PR eligibility and draft behavior in the actual account; do not assume they match human PRs.
2. In GitHub configure required CI and Web checks plus the agreed independent approval policy, with stale approvals dismissed and no worker bypass. Inspect actual rulesets before claiming enforcement. A bot's comment may not count as an approving review.
3. Open a non-production smoke PR, mark ready if needed, and observe an actual Codex review. Record URL, head SHA, actor and completed review timestamp. An eyes reaction is only acknowledgement.
4. Push a small amendment and verify the selected trigger refreshes the review for the new head. Test failure/recovery and close the smoke PR without merging test changes.
5. If native triggers do not cover the worker identity, use `python tools/delivery/request_review.py --repo Pietrols/Quantic-Studio --pr NUMBER`. The script explicitly posts a review request via the authenticated GitHub CLI, with one marker per head SHA. Run it only after publishing a reviewable PR. It does not enable repository settings.

This session supplies configuration instructions and the request helper. It does not claim that account-level settings, protection rules or automatic reviews were activated.

## Manager event loop

Track `(repository, PR number, head SHA)` as identity. After CI and internal checks pass, set review state requested. Observe reviews/comments/check runs without repeatedly posting requests. If the head changes, reset acceptance and associate findings with their reviewed SHA. Do not reuse an approval from another commit without a documented scope check and refreshed relevant verification.

For auth/rate-limit/outage errors retain a pending checkpoint, retry with bounded backoff and then report the blocker. No success-by-timeout. A closed/replaced PR is terminal. If native review is enabled, avoid duplicate explicit triggers; use the helper only for the verified fallback or intentional re-review.

After findings: small fix plus regression and rerun; or structured repair task to worker. Close a finding only after reproducing the correction. Distinguish dismissed/accepted-risk/deferred from fixed. Engineering blockers are not cosmetic waivers. Product owner acceptance and PM audit are recorded separately from bot findings.

## Evidence contract

Use `tools/delivery/evidence-template.json` and validate with `python tools/delivery/validate_evidence.py PATH`. It is a structural check, not proof that tests ran. Evidence names the code commit tested, source requirements, commands, exit codes, artifact paths, role sessions and open blockers. Do not try to embed a commit's own SHA in a file within that same commit: generate final review evidence as a CI artifact or PR attachment referencing the tested head, or identify the tested code commit and explicitly account for later documentation-only changes.

The initial supplied template is deliberately incomplete and must fail readiness validation. A reviewer inspects actual CI logs, diff, numerical provenance and screenshots. Same-model reviews and empty findings do not prove correctness.
