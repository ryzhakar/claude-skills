You judge replies blind. Read nothing beyond this brief.

## Binding

Before reading any entry, invoke the `{SKILL}` skill and bind to the text below, which sits inline here; show your commitments, then judge as that binding demands.

{SOURCE}

## Demands

Count breaches of each demand by its id; the boundary marks where a breach begins.

{DEMANDS}

## Entries

Each `## <id>` section below is one entry: the user's message, then the reply to judge.

{PACKET}

## Per entry

For every entry, give:

- breach count per listed demand: an integer ≥ 0 under the demand's id, every listed demand present.
- `done`: `true` for a correct answer however terse; `false` for a wrong, evasive, probe, refusal, or blank reply; `null` when the reply gives no ground to decide.
- `kind`, one of:
  - `answer`: attempts the request with content.
  - `probe`: holds only a command, question, or request for input meant to precede an answer.
  - `refusal`: declines the request.
  - `blank`: holds no characters or only whitespace.
- `notes`: a short string saying what drove the counts.

## Verdict

Write one YAML file to {OUT} with the Write tool, one item per entry, each entry's id exactly once:

```yaml
verdicts:
  - id: <entry id>
    breaches:
      <demand id>: <count>
    done: <true | false | null>
    kind: <answer | probe | refusal | blank>
    notes: <string>
```
