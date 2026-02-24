from hardware.motor_interface import Motor
from hardware.fast_detector_interface import FastDetector
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
        detector: FastDetector,
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

        if velocity_um_per_s <= 0:
            raise ValueError("Computed motor velocity must be positive.")


        scan_time = scan_range / velocity_um_per_s
        planned_samples = int(scan_time * frequency)

        if planned_samples < 5:
            raise ValueError(
                "Scan resolution too low. Increase acquisition frequency or reduce spatial step."
            )

        # -----------------------------
        # Execute fly scan
        # -----------------------------

        # 1. Move to start position
        self.motor.move_absolute(start_pos)

        # 2. Set constant velocity
        self.motor.set_velocity(velocity_um_per_s)

        # 3. Prepare detector
        self.detector.setup(frequency)

        # 4. Trigger acquisition
        self.detector.trigger(planned_samples)

        # 5. Move across full scan range
        self.motor.move_absolute(end_pos)

        # 6. Retrieve acquired data
        intensities = np.array(self.detector.read())

        # 7. Cleanup detector
        self.detector.cleanup()

        n_samples = len(intensities)

        if n_samples == 0:
            raise RuntimeError("Detector returned no data.")

        times = np.arange(n_samples) / frequency

        direction = np.sign(end_pos - start_pos)
        positions = start_pos + direction * velocity_um_per_s * times

        fit_result = fit_gaussian(positions, intensities)

        return {
            "center": fit_result["center"],
            "fwhm": fit_result["fwhm"],
            "amplitude": fit_result["amplitude"],
            "num_points": n_samples,
        }
