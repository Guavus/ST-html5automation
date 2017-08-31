from Utils.SetUp import *
from Utils.utility import *
from classes.Components.TableComponentClass import *
import random

def sortTable(setup,instance,columnName="Name"):
    tableHandle = getHandle(setup,'Dummy_Screen', "table")
    instance.sortTable1(tableHandle, columnName)
    tableHandle = getHandle(setup, 'Dummy_Screen', "table")

    data2 = instance.getTableData1(tableHandle)
    columnIndex = instance.getIndexForValueInArray(data2['header'], columnName)
    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col), col, "", "", "Verify Sorting For ColumnName ="+columnName)
    logger.info("Sorted")
    cdata2 = instance.convertDataToDictWithKeyAsRow(data2)
    return cdata2

try:
    setup = SetUp()
    gridInstance=TableComponentClass()

    #For Special Selection
    getHandle(setup,'Dummy_Screen','c_control')['c_control']['check'][0].click()
    gridInstance.setSpecialSelection(setup.d, [2,5], Keys.SHIFT,getHandle(setup,'Dummy_Screen','table'))
    data = gridInstance.getSelectedRow(getHandle(setup, 'Dummy_Screen','table'))
    getHandle(setup, 'Dummy_Screen','c_control')['c_control']['check'][0].click()

    #For Sorting
    for column in data['header']:
        sortedData = sortTable(setup, gridInstance, columnName=column)
        resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',column)

    #for Normal table function
    tableHandle = getHandle(setup,'Dummy_Screen', 'table')
    data2 = gridInstance.getTableData1(tableHandle, length=20)
    tablemap=gridInstance.getTableDataMap(getHandle(setup,'Dummy_Screen','table'),driver=setup)

except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
