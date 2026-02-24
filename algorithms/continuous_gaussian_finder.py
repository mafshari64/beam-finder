from hardware.motor_interface import Motor
from hardware.detector_interface import Detector
from utils.fitting import fit_gaussian
from config import BeamFinderConfig

import numpy as np


class ContinuousGaussianBeamFinder:
    """
    Full-range continuous fly scan beam centre finder.

    The motor performs a constant-velocity sweep across the full
    search range while the detector acquires data at fixed frequency.

    All spatial units are in microns.
    Scan direction is chosen based on current motor position.
    """

    def __init__(
        self,
        motor: Motor,
        detector: Detector,
        config: BeamFinderConfig,
    ):
        self.motor = motor
        self.detector = detector
        self.config = config

    def find_beam_center(self) -> dict:

        current_pos = self.motor.get_position()

        search_min = self.config.search_range_min
        search_max = self.config.search_range_max
        midpoint = (search_min + search_max) / 2

        # Choose scan direction based on current position
        if current_pos > midpoint:
            start_pos = search_max
            end_pos = search_min
        else:
            start_pos = search_min
            end_pos = search_max

        scan_range = abs(search_max - search_min)

        frequency = self.config.acquisition_frequency
        spatial_step = self.config.spatial_step   # microns

        velocity_um_per_s = spatial_step * frequency

        self.motor.set_velocity(velocity_um_per_s)
        self.motor.move_absolute(start_pos)

        scan_time = scan_range / velocity_um_per_s
        planned_samples = int(scan_time * frequency)

        self.detector.setup(frequency)
        self.detector.trigger(planned_samples)

        self.motor.move_absolute(end_pos)

        intensities = np.array(self.detector.read())
        self.detector.cleanup()

        n_samples = len(intensities)
        times = np.arange(n_samples) / frequency

        direction = np.sign(end_pos - start_pos)
        positions = start_pos + direction * velocity_um_per_s * times

        fit_result = fit_gaussian(positions, intensities)

        return {
            "center": fit_result["center"],
            "fwhm": fit_result["fwhm"],
            "amplitude": fit_result["amplitude"],
            "num_samples": n_samples,
        }
