# main.py

import logging

from config import BeamFinderConfig
from algorithms.coarse_gaussian_finder import CoarseGaussianBeamFinder
# from algorithms.continuous_gaussian_finder import ContinuousGaussianBeamFinder

from simulation.simulated_motor import SimulatedMotor
from simulation.simulated_detector import SimulatedDetector
from simulation.beam_model import GaussianBeamModel


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main():

    setup_logging()

    config = BeamFinderConfig()

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

    # If continuous mode desired:
    # beam_finder = ContinuousGaussianBeamFinder(
    #     motor=motor,
    #     detector=detector,
    #     config=config,
    # )

    result = beam_finder.find_beam_center()

    # -----------------------------
    # Output results
    # -----------------------------

    print("\n=== Beam Finding Result ===")
    print(f"Center (um): {result['center']:.3f}")
    print(f"FWHM  (um): {result['fwhm']:.3f}")
    print(f"Amplitude  : {result['amplitude']:.3f}")
    print(f"Measurements used: {result['num_measurements']}")


if __name__ == "__main__":
    main()
