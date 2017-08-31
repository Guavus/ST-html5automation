from Utils.utility import *

def sortTable(setup,instance,columnName="Name"):
    tableHandle = getHandle(setup,Constants.DUMMY_SCREEN, "table")
    instance.sortTable1(tableHandle, columnName)
    tableHandle = getHandle(setup,Constants.DUMMY_SCREEN, "table")

    data2 = instance.getTableData1(tableHandle)
    columnIndex = instance.getIndexForValueInArray(data2['header'], columnName)
    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col), col, "", "", "Verify Sorting For ColumnName ="+columnName)
    logger.info("Sorted")
    cdata2 = instance.convertDataToDictWithKeyAsRow(data2)
    return cdata2
