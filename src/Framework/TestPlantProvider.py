
from Framework.ITestProject import ITestProject
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.TestPlant.TestSystemCallNotifier import TestSystemCallNotifier
from Framework.Logger.ITestLogger import ITestLogger
from lib.Singleton import Singleton

class TestPlantProvider(Singleton):
    def setup( self, project : ITestProject ) -> None:
        self.__logger = project.logger ()
        self.__system = TestSystemCallNotifier( project.test_system() )
        self.__system.set_notifee( self.__logger )
        self.stream = open( project.log_filename() , "w", encoding=project.log_encoding())
        self.__logger.set_stream( self.stream )

    def system( self ) -> ITestSystem:
        return self.__system

    def logger ( self ) -> ITestLogger:
        return self.__logger

    def tear_down( self ) -> None:
        self.stream.close()

