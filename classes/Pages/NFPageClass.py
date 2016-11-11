from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass
from classes.Components.ContextMenuComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.PieLegendComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.PieComponentClass import *
from classes.Components.SummaryBarComponentClass import *
from classes.Components.SearchComponentClass import *

class NFPageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.measure = MeasureComponentClass()
        self.pielegend = PieLegendComponentClass()
        self.pie = PieComponentClass()
        self.summarybar = SummaryBarComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.searchComp = SearchComponentClass()

    def testComponents(self):
        return ""

