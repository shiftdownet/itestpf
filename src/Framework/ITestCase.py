
from collections.abc import Iterator
import abc

class ITestCase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare(self) -> None:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def steps(self) -> Iterator:# Iterator[bool]: # CPythonは通るが、IronPythonだとエラーになる
        raise NotImplementedError()
    
    @abc.abstractmethod
    def tear_down(self) -> None:
        raise NotImplementedError()
