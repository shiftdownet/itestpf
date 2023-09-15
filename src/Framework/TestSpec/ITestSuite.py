
import abc

class ITestSuite(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def dummy(self) -> None:
        raise NotImplementedError()
