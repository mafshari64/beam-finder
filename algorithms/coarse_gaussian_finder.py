# algorithms/coarse_gaussian_finder.py

import numpy as np
from hardware.motor_interface import Motor
from hardware.detector_interface import Detector
from utils.fitting import fit_gaussian
from config import BeamFinderConfig


class CoarseGaussianBeamFinder:
    """
    Detector readout takes ~5 seconds per measurement.
    Therefore, parameters are chosen to minimise detector reads
    while maintaining robustness to noise.

    Beam finding workflow (slow detector mode):

    1) Directional coarse bracketing search
    2) Fine scan around estimated peak
    3) Gaussian fitting

    All positions are in microns.
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
        self.measurement_count = 0

    def _measure_intensity(self, position: float) -> float:
        self.motor.move_absolute(position)
        intensity = self.detector.read()
        self.measurement_count += 1
        return intensity

    # ---------------------------------------------------------
    # Directional coarse search (minimise detector reads)
    # ---------------------------------------------------------

    def _adaptive_coarse_search(self) -> float:
        """
        Simple coarse search to read as few points as possible while finding rough peak position:
    
        1. Start at x0
        2. Try positive direction
        3. If stays within noise → continue until intensity increases
        4. If intensity drops 3 times before any increase → wrong direction
           → go back to x0 and try negative direction
        5. If intensity drops after increase → peak passed → stop
        """
    
        step = self.config.coarse_step_size
        noise = self.config.noise_level
        search_min = self.config.search_range_min
        search_max = self.config.search_range_max
    
        # --- initial position ---
        x0 = self.motor.get_position()
        I_prev = self._measure_intensity(x0)
    
        best_pos = x0
        best_signal = I_prev
    
        direction = +step   # try positive first
        drop_counter = 0
        found_increase = False
    
        x_prev = x0
    
        while True:
    
            x_next = x_prev + direction
    
            # --- check scan range ---
            if x_next < search_min or x_next > search_max:
    
                # if we were trying positive, try negative
                if direction > 0:
                    self.motor.move_absolute(x0)
                    x_prev = x0
                    I_prev = self._measure_intensity(x0)
                    direction = -step
                    drop_counter = 0
                    found_increase = False
                    continue
                else:
                    break  # both directions exhausted
    
            I_next = self._measure_intensity(x_next)
    
            # --- case: no significant drop ---
            if I_next >= I_prev - noise:
    
                drop_counter = 0
    
                if I_next > best_signal:
                    best_signal = I_next
                    best_pos = x_next
                    found_increase = True
    
            # --- case: significant drop ---
            else:
                drop_counter += 1
    
                # if we never saw increase and drop happens 3 times → wrong direction
                if not found_increase and drop_counter >= 3:
                    self.motor.move_absolute(x0)
                    x_prev = x0
                    I_prev = self._measure_intensity(x0)
                    direction = -step
                    drop_counter = 0
                    continue
    
                # if we already saw increase → peak passed
                if found_increase:
                    break
    
            x_prev = x_next
            I_prev = I_next
    
        return best_pos

    # ---------------------------------------------------------
    # Fine scan
    # ---------------------------------------------------------

    def _fine_scan(self, center_estimate: float):

        half_width = self.config.fine_scan_half_width

        positions = np.linspace(
            center_estimate - half_width,
            center_estimate + half_width,
            self.config.fine_scan_num_points,
        )

        intensities = [
            self._measure_intensity(pos) for pos in positions
        ]

        return positions, np.array(intensities)

    # ---------------------------------------------------------
    # Public workflow
    # ---------------------------------------------------------

    def find_beam_center(self) -> dict:

        self.measurement_count = 0
        self.detector.setup()

        coarse_peak_position = self._adaptive_coarse_search()

        fine_positions, fine_intensities = self._fine_scan(
            coarse_peak_position
        )

        fit_result = fit_gaussian(
            fine_positions,
            fine_intensities,
        )

        self.detector.cleanup()

        return {
            "center": fit_result["center"],
            "fwhm": fit_result["fwhm"],
            "amplitude": fit_result["amplitude"],
            "num_points": self.measurement_count,
        }
