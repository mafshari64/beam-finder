# hardware/motor_interface.py


class Motor:
    """
    abstract interfaces of the real motor controlling the motion stage, i.e. what a motor must do.

    The beam finding algorithm will only use these methods.
    A real hardware implementation or a simulated version must follow this same interface.
    """

    def move_relative(self, distance: float) -> None:
        """
        Move the motor by a relative distance (in microns).

        Distance can be positive or negative.
        """
        raise NotImplementedError

    def move_absolute(self, location: float) -> None:
        """
        Move the motor to an absolute position (in microns).
        """
        raise NotImplementedError

    def get_position(self) -> float:
        """
        Return the current motor position (in microns).
        """
        raise NotImplementedError

    def set_velocity(self, velocity: float) -> None:
        """
        change the motor velocity (in microns per second).
        """
        raise NotImplementedError
