from classes.Pages.BasePageClass import *
from classes.Components.MulitpleDropdownComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Pages.GlobalFiltersPopClass import *
from classes.Components.TreeComponentClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.CBComponentClass import *

class ComparativeClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.dropdown = DropdownComponentClass()
        self.multiDropdown = MulitpleDropdownComponentClass()
        self.table = TableComponentClass()
        self.calendar = CalendarComponentClass()
        self.tree = TreeComponentClass(driver)
        self.timeBar = TimeRangeComponentClass()
        self.wfstart=WorkflowStartComponentClass()
        self.trend=CBComponentClass()
        # Common Components
        BasePopClass.__init__(self,driver)
