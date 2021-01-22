from __future__ import division
from __future__ import unicode_literals
from steppyngstounes.stepper import Stepper
import itertools

__all__ = ["SequenceStepper"]
from future.utils import text_to_native_str
__all__ = [text_to_native_str(n) for n in __all__]

class SequenceStepper(Stepper):
    r"""Stepper that takes a series of fixed steps.

    Parameters
    ----------
    start : float
        Beginning of range to step over.
    stop : float
        Finish of range to step over.
    sizes : iterable of float
        Desired step sizes.  In the event that `start` plus the sum of
        `sizes` will exceed `stop`, the stepper will terminate at `stop`.
    inclusive : bool
        Whether to include an evaluation at `start` (default False)
    record : bool
        Whether to keep history of steps, errors, values, etc. (default False).

    """

    __doc__ += Stepper._stepper_test(StepperClass="SequenceStepper",
                                     stepper_args="sizes=range(1,10000), record=True",
                                     control_error=False,
                                     steps=46,
                                     attempts=46)

    def __init__(self, start, stop, sizes,
                 inclusive=False, record=False):
        self._wantsizes = iter(sizes)
        
        # peek at first value
        peek = next(self._wantsizes)
        if inclusive:
            pushback = [peek, peek]
        else:
            pushback = [peek]
        self._wantsizes = itertools.chain(pushback, self._wantsizes)
        
        super(SequenceStepper, self).__init__(start=start, stop=stop, size=peek,
                                              inclusive=inclusive, record=record)

    def _adaptStep(self):
        """Calculate next step after success

        Returns next step size in sequence.

        Returns
        -------
        float
            New step.

        """
        return next(self._wantsizes)

    def _succeeded(self, error):
        """Determine if most recent attempt failed.

        Returns
        -------
        True
            Fixed steps always succeed.
        error : float
            Error to record. If `error` was None, returns 0.
        """
        if error is None:
            error = 0.
        return True, error
