
import abc

class ITestLogger(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_stream(self, stream) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def start_test(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def start_suite(self, suite_name: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def start_case(self, case_name: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def start_step(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def end_step(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def end_case(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def end_suite(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def end_test(self) -> None:
        raise NotImplementedError()

