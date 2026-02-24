# utils/fitting.py

import numpy as np
from scipy.optimize import curve_fit


def _gaussian(position, amplitude, center, sigma):
    """
    Gaussian model used for fitting.
    """
    return amplitude * np.exp(-(position - center) ** 2 / (2 * sigma ** 2))


def fit_gaussian(positions: np.ndarray, intensities: np.ndarray) -> dict:
    """
    Fit a Gaussian to beam scan data.

    Parameters
    ----------
    positions : array
        Motor positions in micro meter

    intensities : array
        Measured detector intensities

    Returns
    -------
    dict with:
        center : float
        fwhm : float
        amplitude : float
    """

    if len(positions) != len(intensities):
        raise ValueError("Positions and intensities must have same length.")

    if len(positions) < 3:
        raise ValueError("At least 3 points are required for Gaussian fitting.")
    
    # --- Initial parameter guesses ---
    amplitude_guess = float(np.max(intensities))
    center_guess = float(positions[np.argmax(intensities)])

    # 99.7% of Gaussian lies within ±3σ
    sigma_guess = (np.max(positions) - np.min(positions)) / 6.0

    try:
        popt, _ = curve_fit(
            _gaussian,
            positions,
            intensities,
            p0=[amplitude_guess, center_guess, sigma_guess],
            maxfev=5000,  # allow more iterations for stability
        )
    except RuntimeError as e:
        raise RuntimeError(
            "Gaussian fit failed — insufficient signal or poor sampling."
        ) from e

    amplitude, center, sigma = popt

    fwhm = 2.355 * abs(sigma)

    return {
        "center": float(center),
        "fwhm": float(fwhm),
        "amplitude": float(amplitude),
    }
