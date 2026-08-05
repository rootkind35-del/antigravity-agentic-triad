# Sample Review Verdict Outcomes

### Outcome A: `ship`
```text
VERDICT: ship
REASON: Code passes all unit tests, git diff is strictly inside src/utils/sorter.py, and verification commands are adequate.
```

### Outcome B: `fix-first`
```text
VERDICT: fix-first
REASON: Modified file `src/main.py` which was NOT listed in declared Files/Ownership scope.
```

### Outcome C: `rethink`
```text
VERDICT: rethink
REASON: Proposed architecture introduces circular imports that cannot be resolved without redesigning the component boundaries.
```
