
'''
Part 1
A point detector is mounted on a motion stage such that it can move across a beam of x-rays.
The setup looks like the following from above.
 
The beam is expected to be a gaussian profile with a FWHM of ~ 100microns, the detector can be
assumed to be infinitely small. 
You have access to the following interface for controlling the motor stage and the detector:

'''
class Motor:
    def move_relative(self, distance: float) -> None:
        """Move the motor by {distance} microns -> None, relative to its current location.
        Distance can be both positive or negative to move in either direction."""
        # (method body missing in the photo)

    def move_absolute(self, location: float) -> None:
        """Move the motor to {location}, in microns."""
        # (method body missing)

    def get_position(self) -> float:
        """Return the current position of the motor."""
        # (method body missing)

    def set_velocity(self, velocity: float) -> None:
        """Change the velocity of the motor, in microns per second."""
        # (method body missing)


class Detector:
    def setup(self) -> None:
        """Setup the detector so that it is ready to take data."""

    def read(self) -> float:
        """Give the intensity of the x-rays on the detector."""

    def cleanup(self) -> None:
        """Put the detector back into an idle state."""

'''
Reading the detector takes ~5s at each point. Build a minimal project that will find the centre of 
the beam as quickly and as accurately as possible. It is expected that the project will be in use 
for many years and will have to be supported by future developers and so your solution should 
include anything required to make future support as easy as possible.
You will be assessed based on the logical structure of your solution and how maintainable the code
is for future developers. Feel free to write the solution in the programming language you feel
most comfortable in, including pseudocode, and assume that you have access to libraries of common 
maths functions.

Part 2
A new detector has been bought that can take data at speeds up to 10 readings per second,
it also contains an internal clock feature where the detector will continually take readings 
at the requested frequency. The new detector interface looks like:
'''
class NewDetector:
    def __init__(self, frequency: float) -> None:
        # (constructor body not shown in the photo)

    def setup(self) -> None:
        """Setup the detector so that it is ready to take data, with data points taken
        at the supplied frequency (in Hz)"""

    def trigger(self, number_of_readings: int) -> None:
        """Take the supplied number of readings at the frequency supplied at last setup."""

    def read(self) -> list[float]:
        """Give a list of all the intensity readings of the x-rays on the detector
        since it was setup."""

    def cleanup(self) -> None:
        """Put the detector back into an idle state."""
'''
Improve your project so that it can use these new features to find the beam centre faster. 
'''
 
