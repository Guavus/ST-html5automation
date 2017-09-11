from Utils.SetUp import *
from classes.Pages.MRXScreens.DataExtractionScreen import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import DEHelper

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    deScreenInstance = DataExtractionScreenClass(setup.d)

    DE_Flag=exploreScreenInstance.exploreList.launchModule(exploreHandle, "DATA EXTRACTION")
    availableClasses = setup.cM.getNodeElements("availableClassesForDE","class")
    actualClassesOnUI=deScreenInstance.getAllTitle(getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'allspans'),parent='allspans',child='spanText')

    checkEqualAssert(MRXConstants.AvailableClassesOnDE,actualClassesOnUI,message="Verify available classes on Data Extraction page",testcase_id='MKR-1953')

    for class_de,method_de in availableClasses.iteritems():
        clickFlag=deScreenInstance.clickSpanWithTitle(str(class_de),getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'allspans'),child='spanText')
        tableHandle=getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'table')
        tableData=deScreenInstance.table.getTableData1(tableHandle)

        checkEqualAssert(MRXConstants.DE_TABLE_HEADER,tableData['header'],message="Verify table header for class ="+str(class_de))
        expectedListOfMethods=str(method_de['method']).split(',')
        flag = True
        actualListOfMethods=[]
        for row in tableData['rows']:
            actualListOfMethods.append(row[0])
            if row[0] in expectedListOfMethods and flag:
                method = row[0]
                tableHandle = getHandle(setup, MRXConstants.DATAEXTRACTIONSCREEN, 'table')
                tableData = deScreenInstance.table.getTableData1(tableHandle)
                rowIndex = deScreenInstance.table.getRowIndexFromTable(0, tableHandle, method)
                deScreenInstance.table.setSelectionIndex(rowIndex + 1, len(tableData['header']), h=tableHandle['table'],driver=setup.d)

                expected = {}
                expected = DEHelper.setDEFilters(deScreenInstance, setup, method,"validateCancelButton")
                isError(setup)

                file = filesAtGivenPath(Constants.chromdownloadpath)
                if len(file) != 0:
                    removeFileAtGivenPath(Constants.chromdownloadpath)

                deScreenInstance.clickButton("Cancel",getHandle(setup, MRXConstants.DEPOPUP, MRXConstants.ALLBUTTONS))
                button_list = deScreenInstance.getAllButtonText(getHandle(setup,MRXConstants.DEPOPUP,'allbuttons'))
                checkEqualAssert(0,len(button_list),message="On pressing Cancel Data Extraction Window get disappears",testcase_id="MKR-1969")
                file = filesAtGivenPath(Constants.chromdownloadpath)
                checkEqualAssert(0,len(file),message="Verify that for a selected method and with selected filters if the user presses 'Cancel' button on the data extraction window then no data should get extracted :: Selected Method = "+str(method),testcase_id="MKR-1969")
                flag=False

        expectedMethods=deepcopy(expectedListOfMethods)
        expectedMethods.sort()
        actualMethods=deepcopy(actualListOfMethods)
        actualMethods.sort()
        checkEqualAssert(expectedListOfMethods,actualListOfMethods,message="Verify that on clicking on "+str(class_de)+" class all the methods corresponding to "+str(class_de)+" class gets listed :: (Functional without BE)",testcase_id=method_de['testcase'])
        checkEqualAssert(expectedMethods, actualMethods,message="Verify that " + str(class_de) + "class is clickable" + str(class_de),testcase_id='MKR-1953')
        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


