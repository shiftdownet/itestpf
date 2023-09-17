
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.Logger.TestProgressMonitor import TestProgressMonitor
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase

class StructuralTestLogger(TestProgressMonitor):
    def __init__(self):
        super().__init__()
        self.root = {"test": { "result":{"suite":{"passed":0, "failed":0},"testcase":{"passed":0, "failed":0}}, "suites": [] }}
        self.commands_target = None

    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        super().set_stream(stream)

    def log(self, message: str) -> None:
        self.commands_target.append( {
            "command":"log",
            "message":message
        })
        super().log( message )

    def start_test(self) -> None:
        super().start_test()

    def start_suite(self, suite: ITestSuite) -> None:
        self.suite = {"suite":suite.name(), "result":{"judge":"", "passed":0, "failed":0}, "description":suite.description(), "prepare":{"commands":[]}, "testcases":[], "tear_down":{"commands":[]}}
        self.commands_target = self.suite["prepare"]["commands"]
        super().start_suite( suite )

    def start_case(self, testcase: ITestCase) -> None:
        self.case = {"testcase":testcase.name(), "result":{"judge":"", "passed":0, "failed":0}, "description":testcase.description(), "prepare":{"commands":[]}, "steps":[], "tear_down":{"commands":[]}}
        self.commands_target = self.case["prepare"]["commands"]
        super().start_case( testcase )

    def start_step(self) -> None:
        self.step = {"step":self.step_no, "result":{"judge":"", "passed":0, "failed":0}, "commands":[]}
        self.commands_target = self.step["commands"]
        super().start_step()

    def end_step(self) -> None:
        super().end_step()
        self.step["result"]["judge"] = ( "Passed" if self.failed_count_of_command == 0 else "Failed" )
        self.step["result"]["passed"] = self.passed_count_of_command
        self.step["result"]["failed"] = self.failed_count_of_command
        self.case["steps"].append( self.step )
        self.commands_target = self.case["tear_down"]["commands"]

    def end_case(self) -> None:
        super().end_case()
        self.case["result"]["judge"] = ( "Passed" if self.failed_count_of_step == 0 else "Failed" )
        self.case["result"]["passed"] = self.passed_count_of_step
        self.case["result"]["failed"] = self.failed_count_of_step
        self.suite["testcases"].append( self.case )
        self.commands_target = self.suite["tear_down"]["commands"]

    def end_suite(self) -> None:
        super().end_suite()
        self.suite["result"]["judge"] = ( "Passed" if self.failed_count_of_case == 0 else "Failed" )
        self.suite["result"]["passed"] = self.passed_count_of_case
        self.suite["result"]["failed"] = self.failed_count_of_case
        self.root["test"]["suites"].append( self.suite )
        self.commands_target = None

    def end_test(self) -> None:
        super().end_test()
        self.root["test"]["result"]["suite"]["passed"] = self.passed_count_of_suite
        self.root["test"]["result"]["suite"]["failed"] = self.failed_count_of_suite
        self.root["test"]["result"]["testcase"]["passed"] = self.total_passed_count_of_case
        self.root["test"]["result"]["testcase"]["failed"] = self.total_failed_count_of_case

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        result = super().test_variable( variable_name, expected_value )
        self.commands_target.append( {
            "command":"test_variable",
            "variable":variable_name,
            "actual":0,
            "expect":expected_value,
            "result":result
        })
        return result

    def get_value_by( self, variable_name : str ):
        return 0 # 実装不要
