
from Framework.TestPlant.ITestSystem import *
from Framework.Logger.ITestLogger import *
from Framework.TestSpec.ITestSuite import *
from Framework.TestSpec.ITestCase import *

class XmlTestLogger(ITestLogger, ITestSystem):
    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        self.stream = stream

    def log(self, message: str) -> None:
        pass

    def start_test(self) -> None:
        pass

    def start_suite(self, suite: ITestSuite) -> None:
        pass

    def start_case(self, testcase: ITestLogger) -> None:
        pass

    def start_step(self) -> None:
        pass

    def end_step(self) -> None:
        pass

    def end_case(self) -> None:
        pass

    def end_suite(self) -> None:
        pass

    def end_test(self) -> None:
        pass

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        return True

    
