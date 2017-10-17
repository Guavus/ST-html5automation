from classes.Pages.BasePageClass import *
from classes.Pages.BasePopClass import *
from classes.Components.MulitpleDropdownComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *

class UserManagementScreenClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.picker = MulitpleDropdownComponentClass()
        self.dropdown = DropdownComponentClass()
        self.table = TableComponentClass()
        # Common Components
        BasePopClass.__init__(self,driver)
