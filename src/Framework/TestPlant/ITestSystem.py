
import abc

class ITestSystem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def assert_variable(self) -> None:
        raise NotImplementedError()

