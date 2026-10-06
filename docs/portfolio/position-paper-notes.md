# Position paper preparation and verification

Prepared for James Lambert, with the confirmed professional direction of
full-stack development and application security. This is an AI-assisted draft:
James should read, personalize, and verify its reflection before submission.

## Deliverables

- [PDF paper](James_Lambert_Position_Paper.pdf): generated successfully using
  Pandoc and pdfLaTeX; text extraction verified the author, all sections,
  references, and key metrics. Seven pages, including a separate references page.
- [Editable source](position-paper.md): Markdown with PDF formatting metadata.

## Verified word counts

| Body section | Words |
| --- | ---: |
| System Delivery and Integration | 400 |
| Methodology and Performance Evaluation | 450 |
| Professional Development Roadmap | 450 |
| Total body | 1,300 |

Counts use whitespace-separated words in the prose, including in-text citations.
The title, author, headings, formatting commands, and reference list are excluded.
Different word processors may count hyphenated terms differently. Confirm the
instructor's counting convention if one is provided; this preparation does not
claim the instructor approved exclusions or a solo submission.

## Evidence and sources

Project measurements come from
[repository evidence](../evidence/unit8/repository-evidence.md) and its raw
coverage/benchmark reports. They describe the measured local build, not an
unverified final-commit CI result or production deployment.

External sources were consulted on October 5, 2026 (America/Chicago):

- SEI's Architecture Tradeoff Analysis Method report: architectural quality
  attributes and tradeoffs; the paper does not claim a formal ATAM evaluation.
- NIST SP 800-218, SSDF 1.1: security practices integrated into development;
  the paper does not claim full framework compliance.
- OWASP ASVS 5.0.0: a versioned basis for future verification work.
- GitHub Octoverse 2025: TypeScript's ranking by monthly contributor counts,
  not a claim about all developers or employment demand.
- Stack Overflow Developer Survey 2025: AI adoption intentions and accuracy
  distrust among respondents, not among every developer.

The reference list contains source links. The roadmap's milestones are proposed
future commitments, not accomplishments or training already completed.

## Before submission

1. Verify the first-person account, including teammate participation and the
   extent of AI assistance. Replace any wording that does not reflect your experience.
2. Confirm the roadmap's three-, six-, and twelve-month commitments are realistic.
3. Update CI/deployment status if new evidence becomes available. Recheck word
   counts after edits; current gaps are disclosed rather than reported as successes.
4. Confirm required citation style and any course-specific AI assistance disclosure.
5. Open the PDF and inspect page layout, references, and hyperlinks before uploading.
6. Include team names and accurate individual contributions in the overall
   submission documentation when those names are known. No teammate names have
   been invented here.

To regenerate the PDF from the repository root:

```bash
pandoc docs/portfolio/position-paper.md --pdf-engine=pdflatex -o docs/portfolio/James_Lambert_Position_Paper.pdf
```

This uses locally installed document tools and does not change application dependencies.

Suggested commit:
`docs: add Unit 8 position paper and verified PDF`.
