
import abc

class ITestSystem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def test_variable(self, variable_name, expected_value) -> bool:
        raise NotImplementedError()

