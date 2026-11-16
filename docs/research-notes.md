# Research notes

Background reading, literature checks and project context. Newest findings at the top of each section. Anything marked *unverified* comes from abstracts or search results and still needs reading in full.

---

## Project context (as of 2026-11-14)

- **Goal:** reconstruct a magnetic field from sparse 3-axis Hall-sensor readings with a PINN, and pick the next measurement point by ensemble disagreement (active sampling).
- **Physics:** in a source-free region, B = −∇φ and ∇²φ = 0. The network outputs φ; loss = data loss on B + Laplace residual at collocation points. Curl-free by construction; divergence-free is enforced softly by the Laplace loss.
- **Stages and gates:** (1) simulation with Biot-Savart, comparing plain NN, PINN and GP, with active vs random vs grid sampling, target Dec 5-10 2026; (2) hand-placed grid template, TLV493D or MLX90393 on an ESP32, under $50; (3) optional XY gantry.
- **Time budget:** about 4-5 h/week.
- **Why:** long-term goal is working in fusion, where knowing confining fields from limited measurements is a real problem. Target audience for the result: Waterloo co-op applications opening in January.

---

## Literature map

### 1. Closest prior work: PINN field mapping

- **Yu et al. (2026), *3D Magnetic Field Reconstruction and Mapping with PINNs*,** arXiv:2605.25640. PINN reconstruction of a 3D field for precision muon experiments, SIREN-style network, measurements from a motorized stage, plain-network ablation. Closest paper to this project. [arXiv](https://arxiv.org/abs/2605.25640) · [related talk slides](https://indico.ihep.ac.cn/event/29862/contributions/224265/attachments/104530/141147/Physics-Informed%20Neural%20Networks%20for%203D%20Magnetic%20Field%20Reconstruction%20in%20Precision%20Muon%20Experiments-7-12.pdf)
  - To check when reading: do they choose measurement points adaptively at all? Do they compare against a GP? What sample counts and noise levels?
- **Livermore et al. (2024), *Reconstructions of Jupiter's magnetic field using PINNs*,** MNRAS 533. PINN on sparse Juno data, potential-field formulation. [PDF](https://eprints.whiterose.ac.uk/id/eprint/217265/1/stae1928.pdf)

### 2. The baseline to take seriously: physics-informed Gaussian processes

This is the most important finding so far. GPs for magnetic fields with **curl-free kernels built from a scalar potential** are well established, mostly in indoor-positioning and robotics work. A plain RBF GP baseline would be a weak comparison; reviewers and interviewers who know this area will expect the curl-free GP.

- **Solin, Kok, Wahlström, Schön, Särkkä (2018), *Modeling and interpolation of the ambient magnetic field by Gaussian processes*,** IEEE Trans. Robotics. Models B = −∇φ with a GP prior on φ, exactly the same physics assumption as our PINN. [arXiv:1509.04634](https://arxiv.org/abs/1509.04634)
- **Wahlström et al. (2013), *Modeling magnetic fields using Gaussian processes*,** ICASSP. Introduced the curl-free kernel for magnetic fields. [PDF](https://people.isy.liu.se/rt/manko/publications/WahlstromKSG2013.pdf)
- **Jidling et al. (2017), *Linearly constrained Gaussian processes*,** NeurIPS. General recipe for building divergence-free or curl-free GP kernels. [arXiv:1703.00787](https://arxiv.org/abs/1703.00787)
- *Unverified:* GP mapping with a magnetometer array and noisy input positions, relevant to our hand-placement error. [arXiv:2310.16577](https://arxiv.org/abs/2310.16577)

### 3. Active sampling / adaptive measurement

- Uncertainty-driven sampling with GPs (pick the point of maximum posterior variance) is a classic idea in spatial field mapping and robotic information gathering. Example: *Robotic Active Information Gathering for Spatial Field Reconstruction with RRTs and Online GPs* (Sensors, 2019). [PMC6427366](https://pmc.ncbi.nlm.nih.gov/articles/PMC6427366/)
- *Unverified:* active magnetic mapping with quantum sensors for disaster response (2026). [arXiv:2606.25957](https://arxiv.org/abs/2606.25957)
- Ensemble PINNs for uncertainty: *E-PINN* (2022). [arXiv:2209.10195](https://arxiv.org/abs/2209.10195)

### 4. Foundations

- Raissi, Perdikaris & Karniadakis (2019), the original PINN paper, J. Comput. Phys. 378.
- Sitzmann et al. (2020), SIREN, NeurIPS.
- Lakshminarayanan et al. (2017), *Deep Ensembles*, NeurIPS. The standard citation for ensemble disagreement as uncertainty.

---

## What this means for the gap (honest read, first pass)

- "Active sampling for magnetic field mapping" on its own is **not** new: GP variance-driven sampling already does it, with the same physics built into the kernel.
- What may still be new or at least useful: **ensemble-PINN active sampling compared head-to-head against a curl-free GP with variance sampling**, on a **low-cost real rig** with realistic noise and position error. That is a fair, defensible framing, and an honest "the GP wins" result would still be a good project.
- Not yet checked: Google Scholar / arXiv for "active learning" + "PINN" + "magnetic", and whether Yu et al. cite any adaptive-sampling work.

## Suggested changes to the plan (for Miranda to decide)

1. Make the GP baseline a **curl-free (scalar-potential) GP**, and keep a plain RBF GP only as an extra. Cheap to implement: the kernel is the Hessian of an RBF kernel on φ.
2. Add **GP-variance sampling** as a fourth sampling strategy next to ensemble-PINN, random and grid. Without it, "active beats random" doesn't show that the PINN ensemble adds anything.
3. Reword the novelty note in the README to the framing above once Yu et al. is read in full.

## Reading order (about 3-4 hours total)

1. Yu et al. 2026: methods and results sections (1-1.5 h).
2. Solin et al. 2018: sections on the curl-free model (1 h). This is what the GP baseline should be.
3. Raissi et al. 2019: skim sections 1-2 for the loss formulation (30 min).
4. Lakshminarayanan et al. 2017: skim for why ensembles give usable uncertainty (30 min).

## Open questions

- Has anyone done ensemble-disagreement active sampling with a PINN for any field-mapping task?
- At our sample budgets (tens of points), does a curl-free GP simply win? Probably worth knowing early, since it decides how the writeup is framed.
