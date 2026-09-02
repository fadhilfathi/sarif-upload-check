# sarif-upload-check

Verification target for [SIFT](https://github.com/fadhilfathi/sift)'s SARIF emitter.

SIFT must emit SARIF that GitHub Code Scanning actually accepts and renders.
"The upload returned 202" is not evidence of that — a SARIF file can be accepted
and then processed into nothing. This repo closes the loop: the workflow uploads
SIFT's emitted output, waits for processing to finish, then **reads the resulting
alerts back and asserts on them** — count, rule IDs, file paths, line numbers, and
whether suppressions render as dismissed.

Nothing here is a real application. `src/app.py` is a deliberately flawed sample
that exists so uploaded alerts have real file locations to point at. It is never
installed, imported, or executed.

## Layout

| Path | What it is |
| --- | --- |
| `src/app.py` | Location target for the findings |
| `sarif/input.sarif` | Hand-written SARIF, the input to SIFT |
| `sarif/emitted.sarif` | What SIFT produced from it — this is what gets uploaded |
| `.github/workflows/verify.yml` | Uploads, waits, reads alerts back, asserts |

`emitted.sarif` is committed rather than generated in CI because SIFT is private.
Regenerate it with:

```bash
sift triage sarif/input.sarif --out sarif/emitted.sarif --dry-run
```

## Running the check

Actions → **Verify SARIF upload** → Run workflow. It fails if the alerts that come
back do not match what was uploaded.
