# Stakeholder video recording checklist

Use with the [presentation script](stakeholder-video-script.md). Required output:
a 10–15 minute MP4 or accessible hosted video link. This checklist does not claim
a recording exists or that its duration has been verified.

## Prepare the environment

- Follow the root README to configure PostgreSQL, migrations, validated mock
  data, authentication, and the React portal. Use a dedicated demo environment.
- Prepare configured SUPERVISOR and ADMIN accounts. Test both before recording.
  Keep credentials, bearer tokens, signing secrets, and database URLs off screen.
- Rehearse the Commercial Electrician recommendation with maximum results 10,
  minimum score 0, and missing evidence enabled. Note two currently visible
  candidate differences. Scores in the fixed-date preview are not a promise
  about today's live results.
- Use only fictional employee data. Avoid unrelated browser tabs, notifications,
  and personal details in the recording.
- Rehearse DEFERRED feedback and its success confirmation. Explain that feedback
  records an audit decision and does not perform an assignment.
- Rehearse the two-tab stale-version action on a harmless demo profile field.
  Confirm both tabs loaded the old version before the first save; restore the
  original value afterward. If the interaction is unreliable, show the actual
  automated test result and label it accordingly.

## Prepare visible evidence

Keep these tabs ready in order:

1. Title and architecture diagram from the script, rendered at a readable size.
2. Portal login and job list.
3. Employee evidence and recommendation results.
4. Feedback confirmation and profile editing.
5. [Repository evidence](../evidence/unit8/repository-evidence.md).
6. [Backend coverage](../evidence/unit8/backend-coverage.json) and
   [frontend coverage](../evidence/unit8/frontend-coverage-summary.json), or their
   locally generated HTML reports.
7. [Benchmark](../evidence/unit8/recommendation-benchmark.json), with its raw
   samples, environment, 30-run count, persistence counts, and P95.
8. Actual final-commit GitHub Actions summary and deployment evidence, if obtained.
9. Closing slide with James Lambert and the repository link.

For CI, capture the commit SHA, overall conclusion, and Backend, Frontend,
PostgreSQL browser integration, and CI required results. The supplied frontend
summary alone does not establish a successful whole workflow. After committing
workflow changes, use evidence from a new run of that commit.

For deployment, capture the actual environment URL, deployment process/result,
and application health or working workflow. A Vite build or localhost demo alone
is not hosted deployment evidence. If no deployment exists, disclose the gap;
do not put a fabricated deployment image into the video.

## Rehearse and record

- Use a screen recorder you already have; capture the application and narration.
  Do a short audio/legibility test before the full take.
- Target 12 minutes. The script includes time for clicks, scrolling, and pointing
  out evidence. Read naturally and explain the actual candidates on screen.
- Measure a full rehearsal. If under 10 minutes, spend more time explaining the
  visible evidence and system boundaries. If over 15, shorten transitions and
  repeated explanations rather than dropping required content.
- If a request fails, show the actual error briefly and explain it. Resolve the
  problem and record another take if needed. Label prerecorded test evidence as
  such; do not describe a captured test as a current live action.
- Keep the contribution statement brief and factual. Verify the wording reflects
  your experience. It does not establish instructor approval or substitute for
  required independent review.

## Check the exported submission

- [ ] Actual duration is between 10:00 and 15:00.
- [ ] Narration is clear; job evidence, scores, and metrics are legible.
- [ ] Problem, solution architecture, live AI workflow, implementation, performance,
      reliability/scalability limits, and stakeholder value are covered.
- [ ] Every numeric claim agrees with its evidence file and measured build.
- [ ] The narration distinguishes local tests from hosted CI and deployment.
- [ ] No passwords, tokens, secrets, or real personnel data appear.
- [ ] Presenter is identified as James Lambert; contribution wording is accurate.
- [ ] MP4 plays completely, or the hosted link works for the intended reviewer.
- [ ] Actual final filename/link and duration are recorded in the submission.

Suggested filename: `James_Lambert_SkillMatch_Stakeholder_Presentation.mp4`.
Suggested commit for these preparation documents:
`docs: prepare Unit 8 stakeholder video script and recording checklist`.
