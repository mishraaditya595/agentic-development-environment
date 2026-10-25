# Evidence matrix

| Claim | Preferred evidence | If unavailable |
| --- | --- | --- |
| Behavior works | Targeted test or user-path execution | State the unverified scenario |
| No regression | Relevant full suite | Name the skipped suite and reason |
| Build is valid | Project build/typecheck | Report missing tool or failure |
| Repository is compliant | Instructions, diff, and validator | List the unchecked rule |
| Ready to release | Release-specific checks and review | Use `not verified`, never “ready” |
