# simulation/beam_model.py

import numpy as np


class GaussianBeamModel:
    """
    A Gaussian beam model for data fitting.

    This simulates the real x-ray beam.
    The detector will read intensity values from this model.

    Noise can be added to simulate realistic measurements.
    """

    def __init__(self, center, fwhm, amplitude=1.0, noise_level=0.0):
        """
        Parameters
        ----------
        center : float
            True beam centre position (meters)

        fwhm : float
            Beam FWHM (meters)

        amplitude : float
            Peak intensity of the beam

        noise_level : float
            Fractional noise level (e.g. 0.05 = 5%)
        """
        self.center = center
        self.fwhm = fwhm
        self.sigma = fwhm / 2.355
        self.amplitude = amplitude
        self.noise_level = noise_level

    def get_intensity(self, position):
        """
        Return intensity at a given position.

        Gaussian profile + optional random noise.
        """

        # Ideal Gaussian signal
        signal = self.amplitude * np.exp(
            - (position - self.center) ** 2 / (2 * self.sigma ** 2)
        )

        # Add Gaussian noise (if noise_level > 0)
        if self.noise_level > 0:
            # noise standard deviation where typical fluctuations are "noise_std" (eg ±5%) of peak intensity.
            noise_std = self.noise_level * self.amplitude
            # generate (positive or negative) random noise to mimic measurement fluctuations. 
            noise = np.random.normal(0.0, noise_std) 
            return signal + noise

        return signal
