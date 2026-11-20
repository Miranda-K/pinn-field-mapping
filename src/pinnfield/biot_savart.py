"""Magnetic field of a circular current loop from the Biot-Savart law.

Geometry: one loop of radius R in the xy-plane, centred on the origin, with
its axis along z. Current flows counter-clockwise seen from +z, so by the
right-hand rule B points in +z at the centre.
"""

import numpy as np

MU_0 = 4e-7 * np.pi  # vacuum permeability, T·m/A


def loop_segments(radius_m: float, n_segments: int) -> tuple[np.ndarray, np.ndarray]:
    """Chop the loop into n straight pieces (a regular polygon inscribed in the circle).

    Returns:
        midpoints: (n, 3) midpoint of each piece, in metres.
        dl: (n, 3) vector along each piece in the current direction, in metres.
    """
    # Vertices on the circle, going counter-clockwise (increasing angle).
    angles = np.linspace(0.0, 2.0 * np.pi, n_segments + 1)
    vertices = np.stack(
        [radius_m * np.cos(angles), radius_m * np.sin(angles), np.zeros_like(angles)],
        axis=1,
    )
    start, end = vertices[:-1], vertices[1:]
    return 0.5 * (start + end), end - start


def loop_field(
    points_m: np.ndarray,
    radius_m: float,
    current_a: float,
    n_segments: int = 1000,
    chunk_size: int = 2048,
) -> np.ndarray:
    """Field B (tesla) of the loop at each point, by summing Biot-Savart over pieces.

    Each piece contributes dB = (mu0·I / 4π) · (dl × r) / |r|³, where r points
    from the piece's midpoint to the field point.

    Points must not sit on the wire: |r| → 0 there and the field blows up.
    The polygon is a second-order approximation of the circle, so the error
    shrinks roughly like 1/n_segments².

    Args:
        points_m: (m, 3) field points in metres.
        radius_m: loop radius in metres.
        current_a: current in amperes (positive = counter-clockwise seen from +z).
        n_segments: number of straight pieces.
        chunk_size: field points handled per batch, to cap memory at
            about chunk_size × n_segments × 3 floats.

    Returns:
        (m, 3) array of B in tesla.
    """
    points_m = np.asarray(points_m, dtype=float).reshape(-1, 3)
    midpoints, dl = loop_segments(radius_m, n_segments)
    prefactor = MU_0 * current_a / (4.0 * np.pi)

    field = np.empty_like(points_m)
    for start in range(0, len(points_m), chunk_size):
        chunk = points_m[start : start + chunk_size]
        # r[i, j] = vector from piece j to field point i, shape (chunk, n, 3).
        r = chunk[:, None, :] - midpoints[None, :, :]
        r_norm = np.linalg.norm(r, axis=-1, keepdims=True)
        dB = np.cross(dl[None, :, :], r) / r_norm**3
        field[start : start + chunk_size] = prefactor * dB.sum(axis=1)
    return field


def loop_field_on_axis(z_m: np.ndarray, radius_m: float, current_a: float) -> np.ndarray:
    """Exact on-axis field Bz (tesla) of an ideal circular loop, for checking loop_field.

    Bz(z) = mu0·I·R² / (2·(R² + z²)^(3/2)); at the centre this is mu0·I / (2R).
    """
    z_m = np.asarray(z_m, dtype=float)
    return MU_0 * current_a * radius_m**2 / (2.0 * (radius_m**2 + z_m**2) ** 1.5)
