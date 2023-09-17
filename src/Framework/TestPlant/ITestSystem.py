
import abc

class ITestSystem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def test_variable(self, variable_name, expected_value) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_value_by( self, variable_name : str ):
        raise NotImplementedError()
