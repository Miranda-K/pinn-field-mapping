# Learning notes

Newest at top.

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