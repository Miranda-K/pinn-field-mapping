# Sparse Magnetic Field Reconstruction with Physics-Informed Neural Networks and Active Sampling

Reconstructing a full magnetic field map from a handful of Hall-sensor readings, using a neural network that is forced to obey Maxwell's equations and that picks where to measure next.

![Planned Setup](img/cover-render.png)

> **Status: Stage 1 (simulation) in progress.** Nothing below has been measured yet. Every result marked **TBD** will be filled in from real runs, with the config and seed that produced it.

---

## Results

| Question | Result |
| --- | --- |
| PINN vs. plain neural network, error at low sample counts | **TBD** (Stage 1) |
| PINN vs. Gaussian process baseline | **TBD** (Stage 1) |
| Active sampling vs. random / grid: measurements needed to reach the same error | **TBD** (Stage 1) |
| Do the simulation conclusions hold on real Hall-sensor data? | **TBD** (Stage 2) |

<!-- Headline figure goes here once it exists:
![Reconstruction error vs. number of measurements](results/figures/error_vs_samples.png)
-->

*Figure placeholder: reconstruction error vs. number of measurements for each model and sampling strategy.*

---

## Why I'm building this

I've cared about clean energy and the health of the planet for as long as I can remember. In grade 6, a nature documentary introduced me to nuclear fusion, and I couldn't stop talking about it. A lot of people still haven't heard that it's possible. I want to work in fusion.

Fusion devices like tokamaks and stellarators confine plasma with carefully shaped magnetic fields, and knowing those fields precisely, from a limited number of measurements, is a real engineering problem. This project tackles a desk-scale version of it: how few measurements do you need to reconstruct a field accurately, and can a model tell you where to measure next?

---

## Method

**Physics.** In a region with no currents or magnetic material, the field is curl-free and divergence-free. So it can be written as **B = −∇φ**, where the scalar potential φ satisfies Laplace's equation, **∇²φ = 0**.

**PINN.** The network outputs φ(x, y, z) instead of B. The field comes from automatic differentiation of φ, which makes it curl-free by construction. Training minimizes two losses:

- *Data loss:* predicted B matches the sensor readings at measured points.
- *Physics loss:* ∇²φ ≈ 0 at many random collocation points where there is no data.

**Baselines,** trained on exactly the same points:

- Plain neural network that predicts B directly, with no physics loss
- Gaussian process regression
- Multipole fit (optional)

**Active sampling.** Train an ensemble of small networks. Where they disagree most is where the model is least certain, so that's the next point to measure. Repeat: measure, retrain, pick the next point. Compare against random and grid sampling at the same measurement budget.

**Evaluation.** Reconstruction error on held-out points vs. number of measurements, across several random seeds.

### Hardware

A small hand-wound coil is the field source, and an MLX90393 3-axis Hall sensor measures the field on a plane above it. In Stage 2 the sensor is moved by hand between holes in a grid template. In Stage 3 a motorized XY gantry moves it, so the active-sampling loop can pick each next point and go there on its own.

![System block diagram](docs/img/block-diagram.excalidraw.svg)

*How the parts connect. Dashed = Stage 3 gantry.*

<!-- Mechanical sketch goes here once it's done:
![Mechanical sketch of the Stage 2 template and Stage 3 gantry](docs/img/stage2-mechanical-sketch.png)
-->

Two details matter for clean data:

- **Background cancellation.** At each point the sensor reads with the coil current forward (+I) and reversed (−I). The coil's field flips sign but Earth's field and any field from the rig don't, so (B₊ − B₋) / 2 is the coil field alone.
- **Keeping the rig out of the measurement.** The sensor sits on a long non-magnetic arm, away from the stepper motors and steel parts, and the motors are switched off during each reading.

Parts and prices are in [`hardware/parts-list.md`](hardware/parts-list.md).

---

## Roadmap

The project is staged with go/no-go gates, so each stage ends in a complete, honest result.

- [ ] **Stage 1: Simulation** (target: early December 2026, $0)
  - [ ] Biot-Savart field generator for a circular coil, checked against the analytic on-axis field
  - [ ] Noise model: sensor noise and probe position error
  - [ ] Plain NN, PINN, and GP baselines
  - [ ] Error vs. number of samples plot
  - [ ] Ensemble active sampling vs. random and grid
  - [ ] **Gate 1:** does the PINN beat the plain NN at low sample counts?
- [ ] **Stage 2: Minimal hardware** (about $20-50)
  - [ ] 3D-printed or laser-cut grid template and a small hand-wound coil
  - [ ] MLX90393 3-axis Hall sensor on a QT Py microcontroller, logging to CSV
  - [ ] Background cancellation (coil current flipped +I / −I) and offset calibration
  - [ ] 50-100 hand-placed ground-truth points; train on subsets, test on the rest
  - [ ] **Gate 2:** is the real data clean enough to compare methods? If not, report the sensor-limited result.
- [ ] **Stage 3: Automation** (parts ordered and built alongside Stages 1 and 2)
  - [ ] Motorized XY gantry (GRBL plotter or a used 3D printer) with the sensor on a non-magnetic arm
  - [ ] Active sampling running live: the model picks the next point, the gantry moves there

Progress notes for every session are in [`docs/log.md`](docs/log.md). The full plan is in [`docs/PRD.md`](docs/PRD.md).

---

## How to reproduce

*Planned. These commands don't work yet; they describe the target interface.*

```bash
git clone <this repo>
cd pinn-field-mapping
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run every model and sampling strategy from one config with a fixed seed
python scripts/run_experiment.py --config configs/stage1_coil.yaml --seed 0

# Regenerate all figures in results/figures/
python scripts/make_figures.py
```

---

## Repository layout

```
pinn-field-mapping/
├── README.md
├── requirements.txt          # added with the first code
├── configs/                  # one YAML per experiment (source, noise, sample budget, seed)
├── src/pinnfield/            # library code
│   ├── biot_savart.py        #   field simulation
│   ├── models.py             #   plain NN, PINN, GP wrappers
│   ├── train.py              #   training loops and losses
│   ├── active.py             #   ensemble uncertainty and next-point selection
│   └── evaluate.py           #   error metrics
├── scripts/                  # entry points: run experiments, make figures, log sensor data
├── notebooks/                # exploration only; results come from scripts
├── tests/                    # e.g. Biot-Savart vs. analytic on-axis field
├── results/figures/          # final plots (committed)
├── firmware/                 # microcontroller sensor code (Stage 2)
├── hardware/                 # parts list, diagrams, template CAD, wiring, calibration notes
└── docs/
    ├── PRD.md                # project plan
    ├── log.md                # dated lab log
    ├── learning-notes.md     # background notes
    └── img/                  # figures used in the docs
```

---

## References

1. Yu et al., *3D Magnetic Field Reconstruction and Mapping with Physics-Informed Neural Networks*, arXiv:2605.25640 (2026). Closest prior work: PINN field mapping for a precision physics experiment, including a plain-network ablation.
2. Livermore et al., *Reconstructions of Jupiter's magnetic field using physics-informed neural networks*, Monthly Notices of the Royal Astronomical Society 533 (2024). PINN field reconstruction from sparse Juno spacecraft data.
3. Raissi, Perdikaris & Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378 (2019). The original PINN framework.
4. Sitzmann et al., *Implicit Neural Representations with Periodic Activation Functions* (SIREN), NeurIPS 2020. Sine activations, to try if a standard MLP struggles.
5. Ling, Moebs & Sanny, *University Physics Volume 2*, OpenStax (2016), ch. 12 "Sources of Magnetic Fields". Biot-Savart law and the on-axis field of a current loop, used to check the simulator. Figures reused under CC BY-NC-SA 4.0. https://openstax.org/books/university-physics-volume-2/pages/12-1-the-biot-savart-law

Novelty note: the papers above focus on reconstruction accuracy. Whether uncertainty-driven active sampling for this setting is new still needs a proper literature search, so this repo makes no novelty claim yet.
