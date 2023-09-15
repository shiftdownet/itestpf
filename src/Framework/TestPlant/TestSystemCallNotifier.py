

from TestSystemDecorator import *

class XmlTestLogger(TestSystemDecorator):

    def __init__( self, decoratee : ITestSystem ):
        super().__init__( decoratee )

