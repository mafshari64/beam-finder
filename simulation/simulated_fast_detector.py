# simulation/simulated_fast_detector.py

import numpy as np
from hardware.fast_detector_interface import FastDetector
from simulation.beam_model import GaussianBeamModel
from hardware.motor_interface import Motor


class SimulatedFastDetector(FastDetector):

    """
    A simulated fast detector for continuous acquisition.
    This detector simulates high-frequency data acquisition during a motor sweep.
    It samples the intensity from a GaussianBeamModel at the current motor position at a specified frequency.   
    All spatial units are in microns.
    Note: This is a simplified simulation. 
   """
    def __init__(self, motor: Motor, beam_model: GaussianBeamModel):
        self.motor = motor
        self.beam_model = beam_model
        self.frequency = None
        self._data = []

    def setup(self, frequency: float) -> None:
        self.frequency = frequency
        self._data = []

    def trigger(self, number_of_readings: int) -> None:
        # Simulate sampling during motor motion
        positions = np.linspace(
            self.motor.get_position(),
            self.motor.get_position(),
            number_of_readings
        )

        self._data = [
            self.beam_model.get_intensity(pos)
            for pos in positions
        ]

    def read(self) -> list[float]:
        return self._data

    def cleanup(self) -> None:
        self.frequency = None
        self._data = []