

from Framework.TestPlant.ITestSystem import *
from Framework.Logger.ITestLogger import *
from Framework.TestSpec.ITestSuite import *
from Framework.TestSpec.ITestCase import *

class TextTestLogger(ITestLogger, ITestSystem):
    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        self.stream = stream
        self.step_no = 0

    def log(self, message: str) -> None:
        self.stream.write( message )

    def start_test(self) -> None:
        self.stream.write( "start test\n" )

    def start_suite(self, suite: ITestSuite) -> None:
        self.stream.write( "\tTestSuite : " + suite.name() + "\n" )

    def start_case(self, testcase: ITestLogger) -> None:
        self.stream.write( "\t\tTestCase : " + testcase.name() + "\n" )
        self.step_no = 0

    def start_step(self) -> None:
        self.step_no += 1
        self.stream.write( "\t\t\tStep No : " + str(self.step_no) + "\n" )

    def end_step(self) -> None:
        pass

    def end_case(self) -> None:
        pass

    def end_suite(self) -> None:
        pass

    def end_test(self) -> None:
        self.stream.write( "test end\n" )

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        self.stream.write("\t\t\t\tactual : " +variable_name + "\n\t\t\t\texpect : " + str(expected_value) + "\n")
        return True
