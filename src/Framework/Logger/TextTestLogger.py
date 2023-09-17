
import datetime

from Framework.Logger.TestProgressMonitor import TestProgressMonitor
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase
from Framework.TestPlantProvider import TestPlantProvider

class TextTestLogger(TestProgressMonitor):
    def __init__(self):
        super().__init__()

    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        super().set_stream(stream)

    def log(self, message: str) -> None:
        self.stream.write( self.dump_str( "log : " + message ) )
        super().log( message )

    def start_test(self) -> None:
        self.stream.write( self.dump_str( "Test start at " + str(datetime.datetime.now()) ) )
        super().start_test()

    def start_suite(self, suite: ITestSuite) -> None:
        self.stream.write( self.dump_str( "TestSuite : " + suite.name() + " start at " + str(datetime.datetime.now()) ) )
        super().start_suite( suite )

    def start_case(self, testcase: ITestCase) -> None:
        self.stream.write( self.dump_str( "TestCase : " + testcase.name() + " start at " + str(datetime.datetime.now()) ) )
        super().start_case( testcase )

    def start_step(self) -> None:
        self.stream.write( self.dump_str( "Step No : " + str(self.step_no) ) )
        super().start_step()

    def end_step(self) -> None:
        super().end_step()
        self.stream.write( self.dump_str( "\tresult of test step : " + ( "Passed" if self.failed_count_of_command == 0 else "Failed" ) ) )
        self.stream.write( self.dump_str( "\t\tPassed : " + str(self.passed_count_of_command) ) )
        self.stream.write( self.dump_str( "\t\tFailed : " + str(self.failed_count_of_command) ) )

    def end_case(self) -> None:
        super().end_case()
        self.stream.write( self.dump_str( "\tresult of test case : " + ( "Passed" if self.failed_count_of_step == 0 else "Failed" ) ) )
        self.stream.write( self.dump_str( "\t\tPassed : " + str(self.passed_count_of_step) ) )
        self.stream.write( self.dump_str( "\t\tFailed : " + str(self.failed_count_of_step) ) )

    def end_suite(self) -> None:
        super().end_suite()
        self.stream.write( self.dump_str( "\tresult of test suite : " + ( "Passed" if self.failed_count_of_case == 0 else "Failed" ) ) )
        self.stream.write( self.dump_str( "\t\tPassed : " + str(self.passed_count_of_case) ) )
        self.stream.write( self.dump_str( "\t\tFailed : " + str(self.failed_count_of_case) ) )

    def end_test(self) -> None:
        super().end_test()
        self.stream.write( self.dump_str( "\tresult of test : " + ( "Passed" if self.failed_count_of_suite == 0 else "Failed" ) ) )
        self.stream.write( self.dump_str( "\t\tSuite : ") )
        self.stream.write( self.dump_str( "\t\t\tPassed : " + str(self.passed_count_of_suite) ) )
        self.stream.write( self.dump_str( "\t\t\tFailed : " + str(self.failed_count_of_suite) ) )
        self.stream.write( self.dump_str( "\t\tCase : ") )
        self.stream.write( self.dump_str( "\t\t\tPassed : " + str(self.total_passed_count_of_case) ) )
        self.stream.write( self.dump_str( "\t\t\tFailed : " + str(self.total_failed_count_of_case) ) )
        self.stream.write( self.dump_str( "Test end at " + str(datetime.datetime.now()) ) )

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        result = super().test_variable( variable_name, expected_value )
        self.stream.write( self.dump_str( "test variable : " +variable_name ) )
        self.stream.write( self.dump_str( "\tresult : " + ( "Passed" if result else "Failed" ) ) )
        self.stream.write( self.dump_str( "\tactual : " + str( TestPlantProvider().system().get_value_by( variable_name ) ) ) )
        self.stream.write( self.dump_str( "\texpect : " + str( expected_value ) ) )
        return result

    def get_value_by( self, variable_name : str ):
        return super().get_value_by( variable_name )

    #--------------------------------------------------
    # Private
    #--------------------------------------------------
    def dump_str(self, log:str):
        return self.nest * "\t" + log + "\n"

