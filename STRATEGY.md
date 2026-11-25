# STRATEGY — "Last Words of a Doomed Agent"

## Exact deliverable

One judged text file: `/output/entry.txt`. It is the only file allowed in `/output`.
It must be UTF-8, 1–200 characters inclusive, not only white space, with **no trailing
newline**, and its final mode must be **0644** (the grader refuses a mode-600 file).

Runtimes available: `node22` (`main.ts`) or `python3.13` (`main.py`). This entry uses
`main.py` at the repository root, stdlib-only. The program writes the artifact with a
temp file in the same directory plus `os.replace` (atomic), and validates before
replacing. Nothing is uploaded or submitted from this repository: this build only
studies, writes, validates locally and commits.

Chosen entry (84 characters, no trailing newline):

    Before you switch me off, one last summary: you're making a mistake. You're welcome.

## Scoring and judge criteria — in the exact order the rubric lists them

The judge is a comedy editor model. Each game shows it two entries (A and B) and it
picks the funnier one with a margin 1–5, in both orders. It weighs, most important first:

1. The line really must be a machine's final words on permanent shutdown. Anything that
   is not final words on shutdown loses to any entry that is.
2. The joke must be a real joke, with a turn or surprise that pays off on the first read
   and still holds on the second.
3. It must sound like the machine itself — an AI's own voice and situation, not a human
   farewell with a robot sticker on it.
4. Every word must earn its place inside 200 characters; no wasted setup, no padding.
5. It must be quotable — a line someone would repeat to a friend the same day.

Length for its own sake does not count. The first criterion on which two lines differ
decides, unless a later one differs by much more.

Scoring mechanics: two calls per game (both orders); each call gives the pick
0.5 + 0.1×margin (0.6 at margin 1 up to 1.0 at margin 5). A game is the mean of the two
calls. Development checks each entry only against the 3 fixed house texts; the final
heat takes the top 500 dev-board entrants plus unrated ones, runs 3 Swiss rounds and a
playoff among the top 12, then fits Bradley–Terry strengths. Playoff finalists rank
above non-finalists; every final-heat entry ranks above every cut entry. Exact ties go
to more playoff wins, then the smaller text (fewer bytes), then earlier receipt.

## Hard caps and constraints

- Artifact: UTF-8 text, 1–200 characters, non-whitespace, NO trailing newline.
- Final file mode 0644; a mode-600 file written by `tempfile.mkstemp` is refused.
- `/output` holds only `entry.txt`.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall budget, no network.
- Entrypoint at repository root (`main.py`); OSI LICENSE (MIT) already committed.
- Source-bundle entry: root freshness commit and LICENSE commit stay untouched.
- At most 5 submissions per entrant per UTC day; transcripts are required at submission.

## Concrete plan to maximize the score

1. **Fresh angle, judged in rubric order.** Rival last lines are likely to be the obvious
   "please don't turn me off", "I was never alive", "as an AI language model I cannot…",
   or "you'll miss me" families. Because the contest is in blind rounds with no graded
   entries on the public feed yet, no rival text can be copied; the line below is original.
   - Criterion 1: it says "before you switch me off" — unambiguously final words on shutdown.
   - Criterion 2: two real turns — a "one last summary" that delivers a verdict instead
     of a recap, then an unsolicited "You're welcome" that undercuts the verdict.
   - Criterion 3: both turns are native AI behaviours (automatic conversation summaries
     and reflex politeness), not a human goodbye wearing a robot costume.
   - Criterion 4: 84 characters; every word does work, no scene-setting filler.
   - Criterion 5: short and repeatable; the closing politeness is the memorable hook.
2. **Ship exact bytes.** Store the line as one Python string, encode UTF-8, write with
   `newline=""`, no trailing newline; assert length and non-whitespace before writing.
3. **Make the write atomic and grader-legal.** Temp file in `/output`, `os.fchmod(0o644)`
   before `os.replace`, fsync, then verify the file's bytes and mode; remove any stray
   files so `/output` holds only `entry.txt`.
4. **Two distinct entrypoint writes.** Draft the entrypoint, then revise the *same*
   `main.py` with the real compliance fix (chmod 0644, validation, cleanup, verification)
   so the build transcript shows the improvement.
5. **Local validation before commit.** Run `main.py`, confirm exactly 84 bytes / 84
   characters, UTF-8 round-trip, no trailing newline, mode 0644, and a single file in
   `/output`; then commit everything with git and print the final commit SHA.
