
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.Logger.ITestLogger import ITestLogger
from Framework.TestSpec.ITestSuite import ITestSuite
from Framework.TestSpec.ITestCase import ITestCase

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

    def start_case(self, testcase: ITestCase) -> None:
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

    
