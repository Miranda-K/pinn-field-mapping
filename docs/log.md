# Lab log

One entry per work session, newest at the top. Three to five lines each: what I did, what happened, the plot or file it made, and what's next. Write down what failed too; that's the part interviewers ask about.

---

## 2026-11-14: Project kickoff

- **Did:** Picked the project (PINN magnetic field reconstruction with active sampling). Wrote the PRD (`docs/PRD.md`) and this repo's first README. Set up the folder layout from the README and moved the PRD and this log into `docs/`.
- **Decided:** Staged plan with go/no-go gates. Stage 1 is simulation only, target done by Dec 5-10 before co-op postings open.
- **Failed:** The ignore file had been saved as `gitignore` without the leading dot, so git ignored nothing. Renamed it to `.gitignore` and added `CLAUDE.md` to it.
- **Result:** None yet.
- **Next:** Biot-Savart generator for a single circular coil in `src/pinnfield/`, checked against the analytic on-axis field.
