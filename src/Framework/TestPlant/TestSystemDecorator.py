

from ITestSystem import *

class TestSystemDecorator(ITestSystem):
    def __init__( self, decoratee : ITestSystem ):
        self.decoratee = decoratee

    def assert_variable(self) -> None:
        pass
    

