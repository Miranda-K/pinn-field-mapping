# Lab log

Control K + V to view preview (VS code)

## 2026-11-19: Biot-Savart coil field generator

Built my first real code: a simulator for the magnetic field of a single wire loop (`src/pinnfield/biot_savart.py`), plus tests in `tests/test_biot_savart.py`.

- It chops the loop into 1000 straight pieces and adds up each piece's field (Biot-Savart). The only exact answer I can check against is on the loop's axis, and the tests compare to that.
- All 5 tests pass!: centre field, on-axis Bz, zero sideways field on axis, error shrinking with more pieces, chunking giving the same answer.
- A 5 cm, 1 A loop gives about 12.6 µT at the centre, which is weaker than Earth's field (~50 µT). That matters for picking a source and sensor in Stage 2.
- The field blows up on the wire itself, so measurement points have to stay away from the coil, which is the same rule the PINN needs anyway.

Next: noise model (sensor noise + probe position error).


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
 