# PRD: PINN Magnetic Field Mapping with Active Sampling

Miranda Kong · Draft v0.1 · November 14, 2026 · Status: Stage 1 not started

## 1. Summary

Reconstruct a 2D (later 3D) magnetic field from a small number of Hall-sensor measurements using a physics-informed neural network (PINN) that enforces Maxwell's equations in source-free regions, and choose where to measure next using model uncertainty (active sampling). Validate first in simulation, then on a low-cost hand-positioned hardware rig. A motorized gantry is optional.

## 2. Problem and motivation

Measuring a field on a dense grid is slow and costly. Fusion devices, accelerator magnets, and precision physics experiments all need accurate field knowledge from limited measurements. Published work shows PINNs can reconstruct fields from sparse data. This project tests whether uncertainty-driven sampling reduces the number of measurements needed, on a low-cost setup.

## 3. Goals

- Show, in simulation, that a PINN reconstructs the field more accurately than a plain neural network at low sample counts.
- Show that active sampling reaches a target error with fewer measurements than random or grid sampling.
- Reproduce the comparison on real sensor data from a simple physical rig.
- Publish a clean, reproducible repo with a short writeup.

## 4. Non-goals

- Matching lab-grade accuracy or replacing commercial field mappers.
- Full 3D volume mapping in the first version.
- A motorized gantry (optional stretch only).
- Claiming novelty beyond what a literature check supports.

## 5. Research questions and hypotheses

1. Does a PINN beat a plain NN, a Gaussian process, and a multipole fit when data is sparse and noisy? Hypothesis: yes at low sample counts.
2. Does ensemble-disagreement active sampling beat random and grid sampling on error versus number of measurements? Hypothesis: yes, by a meaningful margin.
3. Do the simulation conclusions hold on real, imperfect sensor data? Unknown, and an honest negative result is acceptable.

## 6. Approach: staged with go/no-go gates

**Stage 1: Simulation (no cost).**

- Biot-Savart generator for a single coil or bar magnet (NumPy), with sensor noise and position error.
- Models: plain NN, PINN (predict scalar potential, get B by autodiff in PyTorch), Gaussian process baseline, optional multipole fit.
- Active sampling with an ensemble of small networks.
- Gate 1: the PINN beats the plain NN at low sample counts. If not, debug before buying anything.

**Stage 2: Minimal hardware (under about $50).**

- Printed or laser-cut grid template, weak magnet or small coil, 3-axis Hall sensor (for example TLV493D or MLX90393) on an ESP32 or Arduino.
- Background-field subtraction, offset calibration, about 50 to 100 measured grid points as ground truth.
- Gate 2: real-data results are consistent enough to compare methods. Otherwise report the sensor-limited result.

**Stage 3: Automation (optional).** Motorized XY gantry to run active sampling live.

## 7. Requirements

- Data generator with configurable noise, source type, and sample budget.
- One training script per model, run from a single config.
- Evaluation script that outputs error versus number of measurements for every method and sampling strategy.
- Firmware and logging script for the sensor, saving CSV with position, reading, and timestamp.
- Calibration procedure documented step by step.
- All results reproducible from one command and a fixed random seed.

## 8. Success metrics

These are targets to tune once Stage 1 gives real numbers.

- PINN error lower than plain NN error at the smallest sample budgets, reported as a ratio.
- Active sampling reaches the same error as random sampling with noticeably fewer points (target: 30 to 50 percent fewer).
- Real-data test error reported with uncertainty, across several random train/test splits.
- Repo runs end to end on a fresh machine.

## 9. Timeline (about 3 to 5 hours per week)

| Week | Work |
| --- | --- |
| 1 | Biot-Savart generator, noise model, GP baseline |
| 2 | Plain NN and PINN, first error-vs-samples plot |
| 3 | Active sampling, Gate 1 decision |
| 4 | Hardware rig, sensor wiring, calibration |
| 5 | Real data collection and comparison, Gate 2 decision |
| 6 | Writeup, README, demo video |

Stretch: gantry automation after week 6.

## 10. Budget

Stage 1: $0. Stage 2: about $20 to $50 (sensor breakout, microcontroller if needed, magnet or coil, printed template). Stage 3: about $100 to $250 more.

## 11. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Sensor offsets, noise, Earth's field | Background subtraction, calibration step, weak source |
| Hand-placement position error | Fixed grid template, include position noise in simulation |
| Sensor saturation near magnet | Measure at distance, use weak magnet or coil |
| PINN does not beat GP on real data | Report honestly, analyze why |
| Laplace assumption breaks near source | Keep sampling region away from source body |
| Running out of time | Gates let you stop at a complete result after Stage 1 or 2 |

## 12. Related work to read and cite

- Yu et al., 3D Magnetic Field Reconstruction and Mapping with Physics-Informed Neural Networks, arXiv:2605.25640 (May 2026). Closest prior work.
- Livermore et al., Reconstructions of Jupiter's magnetic field using physics-informed neural networks, MNRAS 533 (2024).
- Gaussian-process magnetic field mapping literature (to find).
- Do a proper literature search on active sampling for field mapping before claiming novelty.

## 13. Open questions

- Single coil or bar magnet as the first source?
- Which Hall sensor, given the field strength of the chosen source?
- Is there a Waterloo prof or lab willing to give feedback or lend a better sensor?

## 14. Progress log

Keep dated entries here or in the repo's lab notebook: what was done, result, plot, next step.
