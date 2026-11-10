# Security Policy

## Supported versions

Security fixes are applied to the default branch (`main`). Older snapshots and archived
baselines are provided for reference and are not maintained release lines.

## Reporting a vulnerability

**Do not report exploitable vulnerabilities in a public GitHub Issue, discussion, pull
request, or commit.**

1. If GitHub's **Private vulnerability reporting** feature is enabled for this repository,
   use the repository's **Security → Advisories → Report a vulnerability** flow.
2. If that feature is unavailable, contact the repository maintainer privately through
   the contact method listed on the maintainer's GitHub profile. Do not include exploit
   details in a public message.
3. Include the affected path/version, impact, reproducible steps or a proof of concept,
   and any suggested mitigation. Redact credentials, personal data, and production
   identifiers from the report.

Please allow the maintainer reasonable time to acknowledge and investigate the report
before public disclosure. A coordinated disclosure timeline will be agreed with the
reporter based on severity and remediation complexity.

## Scope and expectations

Reports are especially useful for:

- exposed credentials, tokens, private keys, or personal information;
- authentication, authorization, or access-control bypasses;
- unsafe file upload, path traversal, injection, or remote code execution;
- vulnerable dependencies or GitHub Actions workflows;
- supply-chain risks affecting project templates or generated projects.

Automated scanner output without a demonstrated security impact may be triaged as a
dependency or maintenance issue rather than a vulnerability.

## Repository safeguards

The root CI workflows include Gitleaks secret scanning and OSV-Scanner dependency
scanning. The workflow source also defines pull-request validation jobs. Whether pull
requests and particular status checks are currently enforced as merge requirements is
a GitHub ruleset setting and must be verified in repository Settings → Rules → Rulesets.
The last recorded configuration snapshot and its verification limitation are documented
in [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md).

These controls reduce risk but do not guarantee that every vulnerability is detected.
Do not submit real secrets or production data in tests, fixtures, issues, or pull requests.
