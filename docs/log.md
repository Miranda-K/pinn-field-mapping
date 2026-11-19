# Lab log

Control K + V to view preview (VS code)

## 2026-11-18: How neural networks learn

Watched an intro video on how neural networks learn and reminded me of a polynomial-fitting activity from lin alg (notes in `docs/learning-notes.md`, diagram in `docs/img/`).

- Computing and learning are 2 separate steps. Each layer computes f(Wx + b), then gradient descent nudges W and b downhill on the error.
- The polynomial activity is the same matrix-vector product as a layer, but solved exactly with A⁻¹b.
- To make it a PINN specifically, I mostly change the error: data error + λ × physics error.

Next: 3Blue1Brown chapter 3 (backprop), then start the Biot-Savart generator.
 
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
 