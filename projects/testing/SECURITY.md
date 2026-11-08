# Security Policy — testing

## Supported versions
Security fixes are applied to the default branch. State supported release branches here.

## Reporting a vulnerability
Do not publish exploit details in public issues, discussions, pull requests, or commits.
Use GitHub **Security → Advisories → Report a vulnerability** if private vulnerability
reporting is enabled. Otherwise contact the project maintainer privately using the
contact method published in the maintainer's profile.

Include affected versions/paths, impact, reproduction steps, and mitigation suggestions.
Remove credentials, personal data, and production identifiers from the report. Coordinate
a reasonable disclosure timeline with the maintainer before public disclosure.

## Scope
Reports involving exposed credentials, access-control bypasses, injection, unsafe uploads,
dependency vulnerabilities, and CI/workflow supply-chain risks are welcome.

## Safeguards
Use synthetic test data, keep secrets out of Git, review Gitleaks and OSV-Scanner results,
and apply least-privilege permissions to automation. These safeguards reduce risk but do
not guarantee that every vulnerability will be detected.
