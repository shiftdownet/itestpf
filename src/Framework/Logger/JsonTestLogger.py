

from Framework.Logger.StructuralTestLogger import StructuralTestLogger
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase

import json

class JsonTestLogger(StructuralTestLogger):

    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        super().set_stream(stream)

    def log(self, message: str) -> None:
        super().log(message)

    def start_test(self) -> None:
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
        # まとめてすべてダンプするとメモリ消費が激しいことが想定されるので、
        # スイート単位でダンプしていく
        self.commands_target = None
        self.stream.write( json.dumps(self.suite, indent=4, ensure_ascii=False) )
        self.suite_separator = ","

    def end_test(self) -> None:
        self.stream.write("] } }")
        # 最後にまとめてダンプする場合は、以下を有効にする＆他のメソッドはすべてスーパークラスの実装を使う
        # self.stream.write( json.dumps(self.root, indent=4, ensure_ascii=False) )

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        super().test_variable(variable_name, expected_value)
        return True

