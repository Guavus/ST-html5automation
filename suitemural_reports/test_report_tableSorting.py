from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *

setup = SetUp()

login(setup, "admin", "admin123")
setup.d.save_screenshot('../screenshots/screenie.png')

tableMap = ReportsHelper.getTableDataMap(setup)

columnName = "Name"
sortedData = ReportsHelper.sortTable(setup, columnName)

resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
checkEqualDict(sortedData,tableMap['rows'],"","","Checking each row")

# Closing the browser
setup.d.close()