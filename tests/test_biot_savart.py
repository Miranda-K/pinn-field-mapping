"""Check the numerical Biot-Savart loop field against the exact on-axis formula."""

import numpy as np

from pinnfield.biot_savart import MU_0, loop_field, loop_field_on_axis

RADIUS_M = 0.05
CURRENT_A = 1.0
# A 1000-piece polygon is off by ~1e-5 relative, so 5e-5 leaves margin.
RTOL = 5e-5


def on_axis_points(z_m: np.ndarray) -> np.ndarray:
    return np.stack([np.zeros_like(z_m), np.zeros_like(z_m), z_m], axis=1)


def test_centre_field():
    B = loop_field(np.zeros((1, 3)), RADIUS_M, CURRENT_A)
    expected = MU_0 * CURRENT_A / (2 * RADIUS_M)
    np.testing.assert_allclose(B[0, 2], expected, rtol=RTOL)


def test_on_axis_bz_matches_analytic():
    z = np.linspace(-0.3, 0.3, 61)
    B = loop_field(on_axis_points(z), RADIUS_M, CURRENT_A)
    np.testing.assert_allclose(B[:, 2], loop_field_on_axis(z, RADIUS_M, CURRENT_A), rtol=RTOL)


def test_on_axis_transverse_field_vanishes():
    # By symmetry, the sideways pieces of dB from opposite sides of the loop cancel on axis.
    z = np.linspace(-0.3, 0.3, 61)
    B = loop_field(on_axis_points(z), RADIUS_M, CURRENT_A)
    centre = MU_0 * CURRENT_A / (2 * RADIUS_M)
    assert np.max(np.abs(B[:, :2])) < 1e-9 * centre


def test_error_shrinks_with_more_segments():
    z = np.array([0.02])
    exact = loop_field_on_axis(z, RADIUS_M, CURRENT_A)[0]
    errors = [
        abs(loop_field(on_axis_points(z), RADIUS_M, CURRENT_A, n_segments=n)[0, 2] - exact)
        for n in (50, 200, 1000)
    ]
    assert errors[0] > errors[1] > errors[2]


def test_chunking_does_not_change_answer():
    rng = np.random.default_rng(0)
    points = rng.uniform(-0.2, 0.2, size=(500, 3))
    one_chunk = loop_field(points, RADIUS_M, CURRENT_A, chunk_size=10000)
    many_chunks = loop_field(points, RADIUS_M, CURRENT_A, chunk_size=37)
    np.testing.assert_allclose(many_chunks, one_chunk, rtol=1e-12, atol=0)
