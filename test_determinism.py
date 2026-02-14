"""Determinism smoke test: submits identical payloads and verifies identical outputs."""

import json
import sys

import requests

API_URL = "http://localhost:8000/apply"
RUNS = 10
TIMEOUT = 10

PAYLOAD = {
    "income_monthly": 5000,
    "dti": 0.35,
    "employment_months": 24,
    "age": 28,
    "has_defaults": False,
}


def main() -> None:
    decisions: list[str] = []
    scores: list[int] = []

    for i in range(1, RUNS + 1):
        resp = requests.post(API_URL, json=PAYLOAD, timeout=TIMEOUT)

        if resp.status_code != 200:
            print(f"Run {i}: FAILED (status {resp.status_code})")
            print(resp.text)
            sys.exit(1)

        try:
            data = resp.json()
        except Exception:
            print(f"Run {i}: FAILED (invalid JSON response)")
            print(resp.text)
            sys.exit(1)

        decision = data.get("decision")
        score = data.get("score")

        if decision is None or score is None:
            print(f"Run {i}: FAILED (missing decision/score)")
            print(json.dumps(data, indent=2, sort_keys=True))
            sys.exit(1)

        decisions.append(decision)
        scores.append(score)
        print(f"Run {i}: decision={decision}, score={score}")

    unique_decisions = sorted(set(decisions))
    unique_scores = sorted(set(scores))
    deterministic = (len(unique_decisions) == 1) and (len(unique_scores) == 1)

    print()
    print(f"Deterministic: {deterministic}")
    print(f"Unique decisions: {unique_decisions}")
    print(f"Unique scores: {unique_scores}")

    sys.exit(0 if deterministic else 2)


if __name__ == "__main__":
    main()
