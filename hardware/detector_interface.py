# hardware/detector_interface.py


class Detector:
    """
    abstract interfaces of the real  x-ray detector.

    The beam finding algorithm will use only these methods.
    A real detector implementation or a simulated version must follow this same interface.
    """

    def setup(self) -> None:
        """
        Prepare the detector so it is ready to take measurements.
        """
        raise NotImplementedError

    def read(self) -> float:
        """
        Return the measured intensity of x-rays on the detector.
        """
        raise NotImplementedError

    def cleanup(self) -> None:
        """
        Put the detector back into an idle state.
        """
        raise NotImplementedError
