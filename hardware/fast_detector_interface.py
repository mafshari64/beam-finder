# hardware/fast_detector_interface.py

class FastDetector:
    """
    Interface for high-frequency continuous acquisition detector.
    """

    def setup(self, frequency: float) -> None:
        """
        Prepare detector for acquisition at given frequency (Hz).
        """
        raise NotImplementedError

    def trigger(self, number_of_readings: int) -> None:
        """
        Acquire the specified number of readings.
        """
        raise NotImplementedError

    def read(self) -> list[float]:
        """
        Return all readings acquired since setup.
        """
        raise NotImplementedError

    def cleanup(self) -> None:
        """
        Put the detector back into an idle state.
        """
        raise NotImplementedError