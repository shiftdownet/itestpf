

from ITestLogger import *

class ITestLogger(ITestLogger):

    def set_stream(self, stream) -> None:
        pass

    def log(self, message: str) -> None:
        pass

    def start_test(self) -> None:
        pass

    def start_suite(self, suite_name: str) -> None:
        pass

    def start_case(self, case_name: str) -> None:
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

