from Utils.SetUp import *
from classes.Pages.MRXScreens.DataExtractionScreen import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import DEHelper
from MRXUtils import UDHelper
from Utils.AvailableMethod import *
import time

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    deScreenInstance = DataExtractionScreenClass(setup.d)

    DE_Flag=exploreScreenInstance.exploreList.launchModule(exploreHandle, "DATA EXTRACTION")
    screen_name=deScreenInstance.getScreenNameFromUI(getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'alllabels'))
    checkEqualAssert(str(MRXConstants.DATAEXTRACTIONSCREENLABLE).strip(),str(screen_name).strip(),message="Verify that the Data Extraction page gets rendered on clicking on its button.",testcase_id='MKR-1951')


    availableClasses = setup.cM.getNodeElements("availableClassesForDE","class")
    availableMethodMappingWithTestCase = setup.cM.getNodeElements("testcaseMappingWithMethod_DE", "method")
    availableMeasureMappingWithTestCase = setup.cM.getNodeElements("testcaseMappingWithMeasure_DE","measure")

    validateTopRowInput=True
    validateSearch=True
    for class_de,method_de in availableClasses.iteritems():
        deScreenInstance.clickSpanWithTitle(str(class_de),getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'allspans'))
        tH=getHandle(setup,MRXConstants.DATAEXTRACTIONSCREEN,'table')
        tD=deScreenInstance.table.getTableData1(tH)
        expectedListOfMethods=str(method_de['method']).split(',')

        for row in tD['rows']:
            if row[0] in expectedListOfMethods:
                method=row[0]
                flag=True
                for i in range(MRXConstants.NUMBEROFFILTERSCENARIOFORDE):
                    tableHandle = getHandle(setup, MRXConstants.DATAEXTRACTIONSCREEN, 'table')
                    tableData = deScreenInstance.table.getTableData1(tableHandle)
                    rowIndex=deScreenInstance.table.getRowIndexFromTable(0,tableHandle,method)
                    deScreenInstance.table.setSelectionIndex(rowIndex+1,len(tableData['header']),h=tableHandle['table'],driver=setup.d)

                    if flag:
                        de_Popup_Header = DEHelper.getDEPopupHeaderText(setup, MRXConstants.DEPOPUP)
                        expected_Popup_Header = str(method) + " - " + "Data Extraction"
                        checkEqualAssert(expected_Popup_Header,de_Popup_Header,message="Verify that on clicking on any of the method, the corresponding Data Extraction window slides down, to extract data based on filters ::  Selected Method = "+str(method),testcase_id="MKR-1958")

                        actualAvailableQuickLinkList = UDHelper.availableQuickLink(setup, MRXConstants.DEPOPUP)
                        checkEqualAssert(MRXConstants.ExpectedQuickLinkList, actualAvailableQuickLinkList,message='Verify that a user is able to select filter time range as "Last 30 days", "Last 7 Days", "Yesterday", "Last 24 Hours", "Last 4 Hours"," Today" or, from calendar  ::  For Method = '+str(method),testcase_id='MKR-1960')

                        actualAvailableMeasureList = UDHelper.availableMeasure(setup, MRXConstants.DEPOPUP,index=0)
                        checkEqualAssert(MRXConstants.ExpectedMeasureForDE, actualAvailableMeasureList,message='Verify that a user is able to select available Measure  ::  For Method = '+str(method),testcase_id='MKR-1961')

                        deHandle = getHandle(setup, MRXConstants.AvailableFilterList)
                        availableFilter = []
                        availableFilter.append(str(deHandle['availablefilter']['option'][0].text))
                        availableFilter.append(str(deHandle['availablefilter']['option'][1].text))
                        availableFilter.append(str(deHandle['availablefilter']['option'][2].text))

                        for dim in deHandle['filterTab']['dimension']:
                            availableFilter.append(str(dim.text))
                        checkEqualAssert(MRXConstants.ExpectedFilterOptionForDE, availableFilter,message="Verify that in the Data extraction window which opens on clicking a method a user can set the time range, choose a Measure, select Top Rows and also apply different filters.",testcase_id='MKR-1959')

                        availableButton=deScreenInstance.getAllButtonText(getHandle(setup,MRXConstants.DEPOPUP,'allbuttons'))
                        checkEqualAssert(MRXConstants.Button_On_DEPOPUP,availableButton,message="Verify Cancel and Extract Data Set buttons on Data Extraction Popup",testcase_id='MKR-1959')

                        inputValue=random.randint(1,int(MRXConstants.MaximumValueForTopRowInput))
                        toprows = deScreenInstance.cm.sendkeys_input(str(inputValue),getHandle(setup, MRXConstants.DEPOPUP,"allinputs"), 0)
                        checkEqualAssert(str(inputValue),toprows,message="Verify Input value for Top Row :: Value Entered = "+str(inputValue), testcase_id="MKR-1962")

                    if validateTopRowInput:
                        availableRowInputScenario = setup.cM.getNodeElements("topRowScenario", "input")
                        for id, scenario in availableRowInputScenario.iteritems():
                            toprows = deScreenInstance.cm.sendkeys_input(str(scenario['value']),getHandle(setup, MRXConstants.DEPOPUP,"allinputs"),0)
                            checkEqualAssert(scenario['expectedValue'],toprows,message="Verify Input value for Top Row :: Value Entered = "+str(scenario['value']),testcase_id=scenario['testcase'])
                        validateTopRowInput=False

                    quicklink = setup.cM.getNodeElements("deScreenFilters", 'quicklink')
                    timeRangeFromPopup, measureFromPopup,toprowsFromPopup = DEHelper.setQuickLink_Measure_TopRows(setup, deScreenInstance, str(i))

                    expected = {}
                    expected = DEHelper.setDEFilters(deScreenInstance,setup,method,str(i),flag)
                    isError(setup)
                    actualtoggleState = DEHelper.getToggleStateForFilters(deScreenInstance, setup, method, str(i), validateSearch)
                    popUpTooltipData = DEHelper.getUDPFiltersToolTipData(MRXConstants.DEPOPUP, setup,method)
                    checkEqualDict(expected, popUpTooltipData,message="Verify Filters Selections On Popup (Functional)",testcase_id="MKR-1964,1965,1966,1967,1968",doSortingBeforeCheck=True)
                    filterFromScreenForDV = UDHelper.mapToggleStateWithSelectedFilter(popUpTooltipData,actualtoggleState)

                    queryFromUI = {}
                    queryFromUI = DEHelper.measureAndDimensionAfterMapping(timeRangeFromPopup, measureFromPopup,method,int(toprowsFromPopup),filterFromScreenForDV)


                    # extract data set
                    file=filesAtGivenPath(Constants.chromdownloadpath)
                    if len(file)!=0:
                        removeFileAtGivenPath(Constants.chromdownloadpath)

                    click_Flag=deScreenInstance.clickButton("Extract Data Set",getHandle(setup, MRXConstants.DEPOPUP, MRXConstants.ALLBUTTONS))
                    expectedTimeEpoch = str(time.time()).split('.')[0]
                    isError(setup)
                    if click_Flag:
                        header, data = DEHelper.getCSVData(method,availableMethodMappingWithTestCase[method]['testcase'])
                        tableHandle = getHandle(setup, MRXConstants.DATAEXTRACTIONSCREEN,'table')
                        tableData1 = deScreenInstance.table.getTableData1(tableHandle)
                        rowIndex1 = deScreenInstance.table.getRowIndexFromTable(0, tableHandle, method)
                        actualTime=tableData1['rows'][rowIndex1][len(tableData1['rows'][rowIndex1])-1]
                        actualTimeEpoch=getepoch(actualTime,tPattern=MRXConstants.TIMEPATTERN,tOffset=MRXConstants.TIMEZONEOFFSET)
                        checkEqualValueAssert(expectedTimeEpoch,str(actualTimeEpoch),message="Verify that the last extraction time gets updated against the method when an extraction is done :: For method ="+str(method),testcase_id="MKR-1981")
                        checkEqualAssert([str(method),str(measureFromPopup)],header,message="Verify csv header for measure ="+str(measureFromPopup) +" Method ="+str(method),testcase_id=availableMeasureMappingWithTestCase[str(measureFromPopup).strip()]['testcase'])
                        checkEqualValueAssert(True,int(toprowsFromPopup)>=len(data),message="Validate the CSV from the Top Rows button :: TopRow Value ="+str(toprowsFromPopup),testcase_id="MKR-3215")

                        #deScreenInstance.clickIcon(getHandle(setup, MRXConstants.DEPOPUP,'icons'), child='closePopupIcon')

                        DEHelper.fireBV(queryFromUI, AvailableMethod.Top_Row, quicklink[str(i)]['table'], header,data,testcase=availableMethodMappingWithTestCase[method]['testcase'])

                    flag = False
                validateSearch=False

            else:
                logger.error("Following Method Not Expected, Check Manually :: %s",str(row[0]))
                resultlogger.error("Following Method Not Expected, Check Manually :: %s", str(row[0]))

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    # raise e
