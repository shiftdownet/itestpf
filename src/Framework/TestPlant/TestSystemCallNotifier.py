

from Framework.TestPlant.TestSystemDecorator import TestSystemDecorator
from Framework.TestPlant.ITestSystem import ITestSystem


class TestSystemCallNotifier(TestSystemDecorator):

    def __init__( self, decoratee : ITestSystem ):
        super().__init__( decoratee )

    def set_notifee( self, notifee : ITestSystem ):
        self.__notifee = notifee

    def test_variable(self, variable_name, expected_value) -> bool:
        self.__notifee.test_variable( variable_name, expected_value )
        test_result = self.decoratee.test_variable( variable_name, expected_value )
        return test_result

    def get_value_by( self, variable_name : str ):
        self.__notifee.get_value_by( variable_name )
        test_result = self.decoratee.get_value_by( variable_name )
        return test_result
