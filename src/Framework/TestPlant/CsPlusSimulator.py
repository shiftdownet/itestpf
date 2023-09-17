

from Framework.TestPlant.ITestSystem import ITestSystem

class CsPlusSimulator(ITestSystem):

    def test_variable(self, variable_name, expected_value) -> bool:
        return False # Logger側で合否判断するので実装不要。

    def get_value_by( self, variable_name : str ):
        return 0

