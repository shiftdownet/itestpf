
import abc

class ITestCase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def dummy(self) -> None:
        raise NotImplementedError()
