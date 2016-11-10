from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass
from classes.Components.ContextMenuComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.PieLegendComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.PieComponentClass import *

class NFPageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        # self.measure = MeasureComponentClass()
        self.pielegend = PieLegendComponentClass()
        self.pie = PieComponentClass()
        # self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()

    def testComponents(self):
        return ""

