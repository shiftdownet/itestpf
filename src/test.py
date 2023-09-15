
from collections.abc import Iterator
import abc

class Test():
    pass

class ITestCase():
    def prepare(self) -> None:
        raise NotImplementedError()
    
    def steps(self) -> Iterator:
        raise NotImplementedError()
    
    def tear_down(self) -> None:
        raise NotImplementedError()
