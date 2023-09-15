


from Framework.TestPlant.ITestSystem import *
from Framework.TestPlant.CsPlusSimulator import *
from Framework.TestPlant.MockSimulator import *
from Framework.TestPlant.TestSystemCallNotifier import *
from Framework.Logger.ITestLogger import *
from Framework.Logger.XmlTestLogger import *
from Framework.Logger.YamlTestLogger import *
from Framework.Logger.TextTestLogger import *
from lib.Singleton import *

class TestPlantProvider(Singleton):
    def __init__(self):
        pass

    def setup( self ) -> None:
        # 生成するロガーを変更する場合、以下を書き換えてください
        #self.__logger = XmlTestLogger()
        self.__logger = YamlTestLogger()
        #self.__logger = TextTestLogger()

        # ロギング先のファイル名
        self.__filename = "./test_log.yaml"

        # ターゲットのテストシステムを変更する場合、以下を書き換えてください
        #test_system = CsPlusSimulator()
        test_system = MockSimulator()

        self.__system = TestSystemCallNotifier( test_system )
        self.__system.set_notifee( self.__logger )

        self.stream = open(self.__filename, "w", encoding='utf-8')
        self.__logger.set_stream( self.stream )

    def system( self ) -> ITestSystem:
        return self.__system

    def logger( self ) -> ITestLogger:
        return self.__logger

    def tear_down( self ) -> None:
        self.stream.close()


