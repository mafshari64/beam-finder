# hardware/detector_interface.py


class Detector:
    """
    abstract interfaces of the real  x-ray detector.

    The beam finding algorithm will use only these methods.
    A real detector implementation or a simulated version must follow this same interface.
    """

    def setup(self) -> None:
        """
        Setup the detector so that it is ready to take data.
        """
        raise NotImplementedError

    def read(self) -> float:
        """
        Give the intensity of the x-rays on the detector.
        """
        raise NotImplementedError

    def cleanup(self) -> None:
        """
        Put the detector back into an idle state.
        """
        raise NotImplementedError
