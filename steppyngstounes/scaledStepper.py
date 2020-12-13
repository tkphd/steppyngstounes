from __future__ import division
from __future__ import unicode_literals
from fipy.steppers.stepper import Stepper

__all__ = ["ScaledStepper"]
from future.utils import text_to_native_str
__all__ = [text_to_native_str(n) for n in __all__]

class ScaledStepper(Stepper):
    r"""Adaptive stepper adjust the step by fixed factors.

    Calculates a new step as

    .. math::

       \Delta_{n+1} = f_\text{grow} \Delta_n

    where :math:`\Delta_n` is the step size for step :math:`n` and
    :math:`f_\text{grow}` is the factor by which to grow the step size.

    On failure, retries with

    .. math::

       \Delta_{n} = f_\text{shrink} \Delta_n

    where :math:`f_\text{shrink}` is the factor by which to shrink the step
    size.
    
    .. note::

        The user must override
        :meth:`~fipy.steppers.stepper.Stepper.calcError` and may override
        :meth:`~fipy.steppers.stepper.Stepper.solve`,
        :meth:`~fipy.steppers.stepper.Stepper.success`, and
        :meth:`~fipy.steppers.stepper.Stepper.failure`.

    Parameters
    ----------
    start : float
        Beginning of range to step over.
    stop : float
        Finish of range to step over.
    tryStep : float
        Suggested step size to try (default None).
    inclusive : bool
        Whether to include an evaluation at `start` (default False)
    minStep : float
        Smallest step to allow (default `(stop - start) *`
        |machineepsilon|_).
    growFactor : float
        Growth factor :math:`f_\text{grow}` (default 1.2).
    shrinkFactor : float
        Shrinkage factor :math:`f_\text{shrink}` (default 0.5).

    """

    __doc__ += Stepper._stepper_test.format(StepperClass="ScaledStepper",
                                            dt=250.,
                                            steps=383,
                                            attempts=478)

    def __init__(self, start, stop, tryStep=None, inclusive=False, minStep=None,
                 growFactor=1.2, shrinkFactor=0.5):
        super(ScaledStepper, self).__init__(start=start, stop=stop, tryStep=tryStep,
                                            inclusive=inclusive, minStep=minStep)
        self.growFactor = growFactor
        self.shrinkFactor = shrinkFactor

    def _shrinkStep(self):
        """Reduce step after failure

        Returns
        -------
        float
            New step.

        """
        return self._sizes[-1] * self.shrinkFactor

    def _calcNext(self):
        """Calculate next step after success

        Returns
        -------
        float
            New step.

        """
        return self._sizes[-1] * self.growFactor

def _test():
    import fipy.tests.doctestPlus
    return fipy.tests.doctestPlus.testmod()

if __name__ == "__main__":
    _test()
        