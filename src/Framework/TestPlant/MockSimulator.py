

from Framework.TestPlant.ITestSystem import *

class MockSimulator(ITestSystem):

    def test_variable(self, variable_name, expected_value) -> bool:
        return ( variable_name == expected_value )





