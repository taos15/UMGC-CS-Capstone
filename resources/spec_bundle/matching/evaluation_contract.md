# Offline evaluation and model-review contract

Offline evaluation is separate from production request handling.

- Use versioned curated expected cases and reviewed supervisor feedback to assess matching.
- Store reproducible expected cases under `data/expected/` or another approved versioned path.
- Report Top-3 relevance/recall against the project target.
- Record `model_version`, dataset version/hash, command, environment, and observed metrics.
- Feedback is evaluation evidence, not direct online training data.
- Weight/model/config changes require explicit review, new versioning, and regression tests.
- Do not claim autonomous retraining, production drift handling, or online learning; they are outside MVP scope.
