from Utils.SetUp import *
from classes.Pages.MRXScreens.DataExtractionScreen import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import DEHelper
import json
from Utils.AvailableMethod import *

def measureAndDimensionAfterMapping(header,data):
    query={}
    query['data']=[]
    query['table_header']=[]
    tmp={}
    headerMapping = ConfigManager().getNodeElements("DE_Table_Pgsql_Mapping", "header")
    methodMapping = ConfigManager().getNodeElements("DE_Table_Pgsql_Mapping", "method")

    for col in header:
        query['table_header'].append(headerMapping[col]['backEnd_ID'])

    for row in data:
        if len(row)==2:
            row[0]=methodMapping[str(row[0]).strip()]['backEnd_ID']
            tmp[row[0]]=row

    methodList=tmp.keys()
    methodList.sort()

    for method in methodList:
        query['data'].append(tmp[method])

    query['count']=len(data)
    return query


def fireBV(dataFromUI,method,table_name,sort_property,testcase=''):
    sleep(1)
    dataFromUI_For_Dump=deepcopy(dataFromUI)
    dataFromUI_For_Dump['measure']=[]
    dataFromUI_For_Dump['dimension'] = []
    dataFromUI_For_Dump['method']=method
    dataFromUI_For_Dump['table_name']=table_name
    dataFromUI_For_Dump['testcase']=testcase
    dataFromUI_For_Dump['sort_property']=sort_property

    import time
    dataFromUI_For_Dump['id'] = str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(dataFromUI_For_Dump))
    with open("DE_DumpFile.txt",mode='a') as fs:
        fs.write(json.dumps(dataFromUI_For_Dump))
        fs.write(" __DONE__" + "\n")

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
    dataFromUI={}
    data = []
    header=[]
    for class_de,method_de in availableClasses.iteritems():
        clickFlag=deScreenInstance.clickSpanWithTitle(str(class_de),getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'allspans'),child='spanText')
        tableHandle=getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'table')
        tableData=deScreenInstance.table.getTableData1(tableHandle)

        header=deepcopy(tableData['header'])
        header.pop(1)
        for row in tableData['rows']:
            if len(row)==3:
                row.pop(1)
                actualTimeEpoch = getepoch(row[1],tPattern=MRXConstants.TIMEPATTERN,tOffset=MRXConstants.TIMEZONEOFFSET)
                row[1]=str(actualTimeEpoch)
                data.append(row)

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

    dataFromUI = measureAndDimensionAfterMapping(header,data)
    fireBV(dataFromUI, AvailableMethod.Top_Row, MRXConstants.DE_PGSQL_TABLE,sort_property="method_name",testcase="MKR-1954,1955,1956,1957")
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


