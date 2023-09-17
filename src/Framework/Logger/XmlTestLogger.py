

from Framework.Logger.StructuralTestLogger import StructuralTestLogger
from Framework.ITestSuite import ITestSuite
from Framework.ITestCase import ITestCase

class XmlTestLogger(StructuralTestLogger):

    #--------------------------------------------------
    # ITestLogger
    #--------------------------------------------------
    def set_stream(self, stream) -> None:
        super().set_stream(stream)

    def log(self, message: str) -> None:
        super().log(message)

    def start_test(self) -> None:
        super().start_test()

    def start_suite(self, suite: ITestSuite) -> None:
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
        super().end_suite()

    def end_test(self) -> None:
        raise NotImplementedError("XMLでダンプする実装がありません。")

    #--------------------------------------------------
    # ITestSystem
    #--------------------------------------------------
    def test_variable(self, variable_name, expected_value) -> bool:
        super().test_variable(variable_name, expected_value)
        return True

