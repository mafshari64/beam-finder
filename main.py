# main.py

import logging

from config import BeamFinderConfig
from algorithms.coarse_gaussian_finder import CoarseGaussianBeamFinder
from algorithms.continuous_gaussian_finder import ContinuousGaussianBeamFinder

from simulation.simulated_motor import SimulatedMotor
from simulation.simulated_detector import SimulatedDetector
from simulation.simulated_fast_detector import SimulatedFastDetector
from simulation.beam_model import GaussianBeamModel


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

def main():

    setup_logging()

    config = BeamFinderConfig()
    config.validate()

    # Switch between slow and continuous mode here
    USE_CONTINUOUS_MODE = False
    
    # -----------------------------
    # Create simulated hardware
    # -----------------------------

    motor = SimulatedMotor(
        initial_position=config.initial_motor_position,
        default_velocity=config.default_motor_velocity,
    )

    # Create beam model (true beam parameters)
    beam_model = GaussianBeamModel(
        center=config.beam_center,
        fwhm=config.beam_fwhm,
        amplitude=config.beam_amplitude,
        noise_level=config.noise_level,
    )

    # -------------------------------------------------
    # Choose beam finding strategy
    # -------------------------------------------------

    if USE_CONTINUOUS_MODE:
        detector = SimulatedFastDetector(
            motor=motor,
            beam_model=beam_model,
        )

        beam_finder = ContinuousGaussianBeamFinder(
            motor=motor,
            detector=detector,
            config=config,
        )

        mode_name = "Continuous Fly Scan Mode"

    else:
        # Create simulated detector
        detector = SimulatedDetector(
            motor=motor,
            beam_model=beam_model,
        )

    # -----------------------------
    # Choose beam finding strategy
    # -----------------------------

    beam_finder = CoarseGaussianBeamFinder(
        motor=motor,
        detector=detector,
        config=config,
    )
    
    mode_name = "Coarse + Fine Scan Mode"

    result = beam_finder.find_beam_center()

    # -----------------------------
    # Output results
    # -----------------------------

    print("\n======================================")
    print(f" Beam Finding Result ({mode_name})")
    print("======================================")
    print(f"Estimated Center (µm): {result['center']:.3f}")
    print(f"Estimated FWHM  (µm): {result['fwhm']:.3f}")
    print(f"Estimated Amplitude : {result['amplitude']:.3f}")
    print(f"Data points used    : {result['num_points']}")
    print("======================================\n")

if __name__ == "__main__":
    main()
