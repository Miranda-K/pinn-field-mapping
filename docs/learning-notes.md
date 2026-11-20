# Learning notes

Newest at top.

---

## Biot-Savart law (2026-11-19)

- Current in a wire → makes a magnetic field around it
- **Biot-Savart law** = how much field 1 tiny piece of wire makes at a point
  - dB = (μ0·I / 4π) · (dl × r) / |r|³
  - **dl** = tiny piece of wire, pointing along the current
  - **r** = arrow from the wire piece → the point you care about
  - **μ0** = **permeability of free space** = 4π × 10⁻⁷ T·m/A, just a constant
- Strength falls off as 1/distance² (the |r|³ on the bottom, but r on top cancels 1 of them)
- Direction = **cross product** dl × r → ⊥ to both the wire and the line to the point
  - **Right-hand rule**: thumb along current, fingers curl the way B wraps around
- Whole loop = add up every tiny piece → integral in theory, a sum in code
- In code: chop circle into 1000 straight pieces, sum all of them
  - More pieces → closer to a real circle, error shrinks ~1/n²
  - NumPy does all pieces at once (**broadcasting**) instead of a for loop
- Only exact answer = on the loop's axis: B = μ0·I·R² / (2·(R² + z²)^(3/2))
  - At the centre (z = 0) → B = μ0·I / (2R)
  - Off-axis has no simple formula (needs **elliptic integrals**) → that's why I sum numerically + test on the axis
  - On axis, sideways parts cancel (each piece has an opposite partner) → only Bz left
- E.g. R = 5 cm, I = 1 A → ~12.6 µT at centre, weaker than Earth's ~50 µT
- Blows up right on the wire (divide by ~0) → keep points away from the coil

Link to my PINN
- Outside the wire, no current → field has no "swirl" (**curl-free**) → can write B = −∇φ
- This simulator = fake "sensor data" + ground truth to score the PINN against
- Still to learn: divergence & curl properly (3B1B video) → why ∇²φ = 0 there

Sources
- [HyperPhysics, Magnetic field of a current loop](http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/curloo.html)
- Griffiths, *Introduction to Electrodynamics*, ch. 5 (Biot-Savart, field of a loop on its axis)

(Also update "Next up": the divergence & curl video is now the main thing to watch.)

---

## How NNs learn + lin alg link (2026-11-18)

Diagram: `docs/img/nn-forward-vs-training.png`

- 2 separate steps: **forward pass** (compute output) vs **training** (adjust weights)

Forward pass (node calc)
- **Pre-activation / weighted sum** z = Wx + b → each entry = 1 node's weighted sum
- **Activation** a = f(z) → becomes the input x for the next layer
- Activation fns = the f
  - Sigmoid → (0, 1), **tanh** → (−1, 1)
  - **ReLU** = max(0, z), modern default
  - **Leaky ReLU** = ReLU but lets a little neg through
  - **Softmax** = last layer, scores → probabilities
  - Job of all of them: add the bend → w/o it, stacked layers collapse into 1 matrix

Training (gradient descent)
- **Loss / error** E = 1 number, how wrong the net is over all training examples
  - Input = the weights, not the data
- **Squared error** E = Σ(pred − true)²
  - Square → errors can't cancel, big mistakes count more, smooth deriv
  - Not related to **difference of squares** a² − b² = (a − b)(a + b), both just square
- **Gradient descent**: w_new = w − η · ∂E/∂w
  - **Learning rate** η = step size → too big overshoots, too small = slow
  - ∂E/∂w computed by **backprop**
- 2 diff functions: network(x) approximates the true fn, E(weights) gets minimized → minimizing E is how you get the approx
- "Intelligence" = huge flexible curve fit → learns the pattern, not just the examples → works on new inputs (**generalization**)

Polynomial activity (lin alg class)
- Row of A = powers of 1 x-value, v = coefficients
- (Av)ᵢ = v₀ + v₁xᵢ + v₂xᵢ² + … → a weighted sum, same op as 1 node
- Solved exactly: v = A⁻¹b. NN can't → too many weights, usually no exact sol'n → learns gradually
- 21 pts, deg 20 → wild swings near edges = **overfitting**
- E = ‖Av − b‖² = squared length of error vector → **least squares** (more pts than coefficients)

PINN = change the error
- E = E_data + λ · E_physics, λ = how much physics counts
- Spring e.g. mu'' + ku = 0 → E_physics = Σ(mu'' + ku)²
- My project: E_physics = Σ(∇²φ)² at **collocation points** (pts w/ no data, just physics check)
- Smooth f (tanh / sine), not ReLU

Sources
- [3B1B ch. 2, Gradient descent](https://www.3blue1brown.com/lessons/gradient-descent)
- [StatQuest, Gradient Descent, Step-by-Step](https://www.youtube.com/watch?v=sDv4f4s2SB8)

---

## Neural networks basics (2026-11-15)

From 3Blue1Brown ch. 1

- E.g. handwritten digits, 28×28 img = 784 px = 784 input neurons
- **Neuron** = holds 1 number (its **activation**), ~0 to 1
- **Layers**: 784 in → 16 → 16 → 10 out (1 per digit), brightest out = guess
  - Middle layers = **hidden layers**
- Each neuron = weighted sum of prev layer + bias → activation fn
  - **Weight** = how much an input matters (can be neg)
  - **Bias** = how easily it turns on
- **Activation function** = squashes the sum
  - **Sigmoid** squashes to 0–1
  - Most nets now use **ReLU** = max(0, x)
- Whole net = 1 big fn w/ ~13k **parameters** (weights + biases)
- **Training / learning** = finding good params (ch. 2–3: **gradient descent**, **backprop**)
- 1 layer = matrix × vector + bias → lin alg!

For my project

- Input = position (x, y, z) → 3 in neurons
- Output = 1 number, **potential φ**
- B = −slope of φ (**gradient**, ∇φ), PyTorch does it automatically (**autograd**)
- Physics loss needs 2nd deriv of φ → ReLU 2nd deriv = 0 → can't use ReLU
- Use smooth activations instead: **tanh** or sine (**SIREN**)

Sources
- [3B1B video](https://www.youtube.com/watch?v=aircAruvnKk) · [written version](https://www.3blue1brown.com/lessons/neural-networks)

---

## Hall sensors (2026-11-15)

- **Hall sensor** = measures B at 1 point
- **Hall effect**: current through thin semiconductor strip → B pushes charges sideways → charge piles up on 1 edge → small voltage
  - **Hall voltage** ∝ B ⊥ to strip
- **3-axis** = elements facing diff directions → Bx, By, Bz
- Digital chips (TLV493D, MLX90393) → ESP32 over **I²C** (2-wire connection)

Problems to plan for
- **Offset** = reading ≠ 0 w/ no magnet → calibrate + subtract
- Earth's field ~50 µT + nearby steel/electronics → **background reading**, subtract
- **Noise** = readings jitter → avg several readings per pt
- **Saturation** = too close to strong magnet → reading maxes out
- **Resolution** = smallest step the chip can report (check datasheets)
  - TLV493D ~0.1 mT/step, ±130 mT range → good for magnets, too coarse for weak fields
  - MLX90393 < 1 µT/step at high gain → better for weak fields
- Pick source first, then sensor

Sources
- [HowToMechatronics, Hall effect](https://howtomechatronics.com/how-it-works/electrical-engineering/hall-effect-hall-effect-sensors-work/)
- TLV493D + MLX90393 datasheets (Infineon, Melexis)

---

## Next up

- 3B1B ch. 2–3 (gradient descent, backprop)
- 3B1B divergence & curl video → the 2 field rules behind φ
- Optional: [Nielsen ch. 1](http://neuralnetworksanddeeplearning.com/chap1.html), free book