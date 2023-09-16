

from Framework.TestPlant.ITestSystem import ITestSystem

class TestSystemDecorator(ITestSystem):
    def __init__( self, decoratee : ITestSystem ):
        self.decoratee = decoratee




