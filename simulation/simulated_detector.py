# simulation/simulated_detector.py

from hardware.detector_interface import Detector
from hardware.motor_interface import Motor
from simulation.beam_model import GaussianBeamModel


class SimulatedDetector(Detector):
    """
    A simulated detector.

    reads intensity from a GaussianBeamModel based on the
    current motor position.

    All spatial units are in microns.
    """

    def __init__(self, motor: Motor, beam_model: GaussianBeamModel):
        self.motor = motor
        self.beam_model = beam_model
        self._is_setup = False

    def setup(self) -> None:
        """
        Prepare the detector for data acquisition.
        """
        self._is_setup = True

    def read(self) -> float:
        """
        Return intensity value at current motor position.
        """
        if not self._is_setup:
            raise RuntimeError("Detector must be setup before reading.")

        # Motor position in microns (hardware units)
        position = self.motor.get_position() 

        return self.beam_model.get_intensity(position)

    def cleanup(self) -> None:
        """
        Put detector back to idle state.
        """
        self._is_setup = False
