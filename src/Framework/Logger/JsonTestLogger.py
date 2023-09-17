

from Framework.Logger.StructuralTestLogger import StructuralTestLogger
from Framework.Logger.TestProgressMonitor import TestProgressMonitor
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase

import json

class JsonTestLogger(StructuralTestLogger):
    def __init__(self):
        super().__init__()

    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        super().set_stream(stream)

    def log(self, message: str) -> None:
        super().log(message)

    def start_test(self) -> None:
        super().start_test()
        self.stream.write("{\"test\": {\"suites\" : [")
        self.suite_separator = ""

    def start_suite(self, suite: ITestSuite) -> None:
        self.stream.write(self.suite_separator)
        super().start_suite(suite)

    def start_case(self, testcase: ITestCase) -> None:
        super().start_case(testcase)

    def start_step(self) -> None:
        super().start_step()

    def end_step(self) -> None:
        super().end_step()

    def end_case(self) -> None:
        super().end_case()

    def end_suite(self) -> None:
        super(StructuralTestLogger, self).end_suite()
        # まとめてすべてダンプするとメモリ消費が激しいことが想定されるので、
        # スイート単位でダンプしていく
        self.commands_target = None
        self.suite["result"]["judge"] = ( "Passed" if self.failed_count_of_case == 0 else "Failed" )
        self.suite["result"]["passed"] = self.passed_count_of_case
        self.suite["result"]["failed"] = self.failed_count_of_case
        self.root["test"]["suites"].append( self.suite )
        self.stream.write( json.dumps(self.suite, indent=4, ensure_ascii=False) )
        self.suite_separator = ","

    def end_test(self) -> None:
        super(StructuralTestLogger, self).end_test()
        self.stream.write("] },")
        self.root["test"]["result"]["suite"]["passed"] = self.passed_count_of_suite
        self.root["test"]["result"]["suite"]["failed"] = self.failed_count_of_suite
        self.root["test"]["result"]["testcase"]["passed"] = self.total_passed_count_of_case
        self.root["test"]["result"]["testcase"]["failed"] = self.total_failed_count_of_case
        self.stream.write( "\"result\":"+json.dumps(self.root["test"]["result"], indent=4, ensure_ascii=False) )
        self.stream.write("}")

        # 最後にまとめてダンプする場合は、以下を有効にする＆他のメソッドはすべてスーパークラスの実装を使う
        # self.stream.write( json.dumps(self.root, indent=4, ensure_ascii=False) )

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        super().test_variable(variable_name, expected_value)
        return True

    def get_value_by( self, variable_name : str ):
        return 0 # 実装不要
