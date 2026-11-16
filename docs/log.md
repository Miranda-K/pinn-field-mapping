## 2026-11-15: Learning about Neural Networks

---
 
## 2026-11-15: Neural networks and Hall sensors
 
Watched 3Blue1Brown's *But what is a neural network?* and read up on Hall sensors (notes in `docs/learning-notes.md`).
 
- A network is one big function. Each layer is a matrix times a vector, plus a bias, through an activation. My PINN needs a smooth activation (tanh or sine), since ReLU's second derivative is zero.
- A Hall sensor reads B from the sideways voltage a field creates in a current-carrying strip. Readings need calibration and background subtraction.
- Seeing my linear algebra class show up was a surprise. It's always felt like pure theory, and seeing it used for something real makes me want to learn more.
Next: 3Blue1Brown chapters 2-3 and the divergence and curl video.
 
## 2026-11-14: Project kickoff
 
Picked the project and wrote the PRD (`docs/PRD.md`) and first README.
 
- Staged plan with go/no-go gates. Stage 1 is simulation only, done by Dec 5-10 before co-op postings open.
- No results yet.
Next: Biot-Savart generator for a single circular coil, checked against the analytic on-axis field.
 