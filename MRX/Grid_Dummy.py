from Utils.SetUp import *
from Utils.utility import *
from classes.Components.TableComponentClass import *
from MRXUtils.Dummy_Helper import *
import random
'''
This script cover testing of below method
1. Set multiple selection on table with shift key
2. Get selected data from table
3. sortTable through column
4. Get data from table (fix length)
5. Get all date from table (with scrolling)
'''

try:
    setup = SetUp()
    gridInstance=TableComponentClass()

    #For Special Selection
    getHandle(setup,'Dummy_Screen','c_control')['c_control']['check'][0].click()
    gridInstance.setSpecialSelection(setup.d, [2,5], Keys.SHIFT,getHandle(setup,Constants.DUMMY_SCREEN,'table'))
    data = gridInstance.getSelectedRow(getHandle(setup, Constants.DUMMY_SCREEN,'table'))
    getHandle(setup, 'Dummy_Screen','c_control')['c_control']['check'][0].click()


    #For Sorting
    for column in data['header']:
        sortedData = sortTable(setup, gridInstance, columnName=column)
        resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',column)


    #for Normal table function
    tableHandle = getHandle(setup,Constants.DUMMY_SCREEN, 'table')
    data2 = gridInstance.getTableData1(tableHandle, length=20)
    tablemap=gridInstance.getTableDataMap(getHandle(setup,Constants.DUMMY_SCREEN,'table'),driver=setup)


except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
