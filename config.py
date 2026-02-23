# config.py

from dataclasses import dataclass


@dataclass
class BeamFinderConfig:
    """
    Configuration parameters for finding the beam centre.

    All distances are in microns unless otherwise stated.

    To modify parameters values, edit values below. No other file needs to be changed.
    """

  # Motor search boundaries
    search_range_min: float = -1000.0   # -1 mm
    search_range_max: float = 1000.0    # +1 mm

    # Adaptive coarse search  (slow detector mode)
    coarse_step_size: float = 100 
    max_coarse_steps: int = 20
    intensity_drop_fraction: float = 0.3  # stop when signal < 30% of peak

    # Fine Gaussian refinement (around rough peak position)
    fine_scan_half_width: float = 150   
    fine_scan_num_points: int = 13 

    # Continuous scan parameters
    acquisition_frequency: float = 1000.0  # Hz
    spatial_step: float = 5    # microns resolution

    # Beam simulation parameters 
    beam_center_m: float = 200 
    beam_fwhm_m: float = 100 
    beam_amplitude: float = 1.0
    noise_level: float = 0.05 # 5% detector noise level (fraction of signal)

    # Desired precision  for fitted beam centre
    center_fit_precision: float = 3 

    # motor parameters
    initial_motor_position: float = 0.0     # microns
    default_motor_velocity: float = 1000.0  # microns/sec