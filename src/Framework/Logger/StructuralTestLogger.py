
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.Logger.ITestLogger import ITestLogger
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase

class StructuralTestLogger(ITestLogger, ITestSystem):

    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        self.stream = stream
        self.step_no = 0
        self.root = {"test": { "suites": [] }}
        self.commands_target = None

    def log(self, message: str) -> None:
        self.commands_target.append( {
            "command":"log",
            "message":message
        })

    def start_test(self) -> None:
        pass

    def start_suite(self, suite: ITestSuite) -> None:
        self.suite = {"suite":suite.name(), "description":suite.description(), "prepare":{"commands":[]}, "testcases":[], "tear_down":{"commands":[]}}
        self.commands_target = self.suite["prepare"]["commands"]

    def start_case(self, testcase: ITestCase) -> None:
        self.case = {"testcase":testcase.name(), "description":testcase.description(), "prepare":{"commands":[]}, "steps":[], "tear_down":{"commands":[]}}
        self.commands_target = self.case["prepare"]["commands"]
        self.step_no = 0

    def start_step(self) -> None:
        self.step_no+=1
        self.step = {"step":self.step_no, "commands":[]}
        self.commands_target = self.step["commands"]

    def end_step(self) -> None:
        self.case["steps"].append( self.step )
        self.commands_target = self.case["tear_down"]["commands"]

    def end_case(self) -> None:
        self.suite["testcases"].append( self.case )
        self.commands_target = self.suite["tear_down"]["commands"]

    def end_suite(self) -> None:
        self.root["test"]["suites"].append( self.suite )
        self.commands_target = None

    def end_test(self) -> None:
        pass

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        self.commands_target.append( {
            "command":"test_variable",
            "variable":variable_name,
            "actual":0,
            "expect":expected_value
        })
        return True
