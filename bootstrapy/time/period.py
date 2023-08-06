from typing import Union, Callable
import enum


class Period:
    """
    Class to handle frequency and tenor.
    """

    def __init__(self, time: Union[str, enum.Enum]):
        if isinstance(time, enum.Enum):
            if time.__class__.__name__ != "Frequency":
                raise ValueError("Time must be of type Frequency")
            self.period = self._frequency(time)
        else:
            raise NotImplementedError(
                "Period for non frequency types is not implemented yet"
            )

    def _frequency(self, time: enum.Enum) -> str:
        match time.name:
            case "ANNUAL":
                return "1Y"
            case "SEMIANNUAL":
                return "6M"
