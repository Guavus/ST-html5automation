from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from MRXUtils.MRXConstants import *
from MRXUtils import ReportHelper
from classes.Pages.ExplorePageClass import *


from classes.Pages.MRXScreens.ReportScreenClass import ReportScreenClass


try:

    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)

    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle, "REPORT")

    reportScreenInstance = ReportScreenClass(setup.d)

    global_filter = setup.cM.getNodeElements("reportFilter", "filter")



###################################  Verify Cross (X) functionality on Filter Area on Report screen
    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
    columnValuesFromTable_beforeFilters = reportScreenInstance.table.getColumnValueFromTable(0, tableHandle)
    tableMap1 = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

    click_status=ReportHelper.clickOnfilterIcon(setup,MRXConstants.REPORTSCREEN,'nofilterIcon')
    expected = ReportHelper.setReportFilter(setup,reportScreenInstance,k=1)
    reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)


    ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'filterClearIcon')
    filterFromScreenAfterClear = ReportHelper.getGlobalFiltersFromScreen(MRXConstants.REPORTSCREEN,reportScreenInstance, setup, flag=False)

    tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
    tableMap2 = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

    checkEqualAssert(MRXConstants.NO_FILTER, str(filterFromScreenAfterClear).strip(),message='Verify No filter text on Report Screen')

    checkEqualAssert(len(tableMap1['rows']),len(tableMap2['rows']),message='Verify Cross (X) functionality on Report Screen :: Before any filter total records in report table ='+str(len(tableMap1['rows']))+' After removing filters total records in report table ='+str(len(tableMap2['rows'])))



############################### Verify Filters(single/multiple) getting applied successfully

    for k in range(0,5):   ##  ==> refers to Report type Filter Scenario in mrx_userlevel_config.xml  under "reportFilter"
        reportName = str(global_filter[str(k)]['reportname']).strip()
        reportType = str(global_filter[str(k)]['reporttype']).strip()
        (deliveredOnDropDownVal, deliveredOnDate) = (str(global_filter[str(k)]['deliveredon']).split("::")[0].strip(),str(global_filter[str(k)]['deliveredon']).split("::")[1].strip())
        (ReportPeriodStartDate, ReportPeriodEndDate) = (str(global_filter[str(k)]['reportperiod']).split("::")[0].strip(),str(global_filter[str(k)]['reportperiod']).split("::")[1].strip())

        filtersToBeApplied_dict = {}
        if reportName != "":
            filtersToBeApplied_dict['reportName'] = reportName
        if reportType != "":
            filtersToBeApplied_dict['reportType'] = reportType
        if  deliveredOnDropDownVal != "" and deliveredOnDate != "":
            filtersToBeApplied_dict['deliveredOn'] = (deliveredOnDropDownVal,getepoch(deliveredOnDate, MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M"))
        if ReportPeriodStartDate != ""  and ReportPeriodEndDate != "":
            filtersToBeApplied_dict['reportPeriod'] = (getepoch(ReportPeriodStartDate, MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M"),getepoch(ReportPeriodEndDate, MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M"))


        if bool(filtersToBeApplied_dict):  ## implies if dictionary is not empty
            tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
            tableMap_beforeFilters = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

            expectedResultSet = []
            expectedResultSet_name = []
            expectedResultSet_type = []
            expectedResultSet_delv = []
            expectedResultSet_period = []

            if "reportName" in filtersToBeApplied_dict.keys():
                expectedResultSet_name += [row[0] for row in tableMap_beforeFilters['rows'].values() if row[1] == filtersToBeApplied_dict['reportName']]

            if "reportType" in filtersToBeApplied_dict.keys():
                expectedResultSet_type += [row[0] for row in tableMap_beforeFilters['rows'].values() if row[2] == filtersToBeApplied_dict['reportType'] and row not in expectedResultSet_name]

            if "deliveredOn" in filtersToBeApplied_dict.keys():
                if filtersToBeApplied_dict['deliveredOn'][0] == "0":
                    deliveredOnValFromDropDown = "After"
                    expectedResultSet_delv += [row[0] for row in tableMap_beforeFilters['rows'].values() if getepoch(row[3], MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN) >= filtersToBeApplied_dict['deliveredOn'][1]]
                elif filtersToBeApplied_dict['deliveredOn'][0] == "1":
                    deliveredOnValFromDropDown = "Before"
                    expectedResultSet_delv += [row[0] for row in tableMap_beforeFilters['rows'].values() if getepoch(row[3], MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN) < filtersToBeApplied_dict['deliveredOn'][1]]

            if "reportPeriod" in filtersToBeApplied_dict.keys():
                expectedResultSet_period += [row[0] for row in tableMap_beforeFilters['rows'].values() if getepoch(row[4].split('-')[0].strip(), MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN) >=filtersToBeApplied_dict['reportPeriod'][0] and getepoch(row[4].split('-')[1].strip(),MRXConstants.TIMEZONEOFFSET,MRXConstants.TIMEPATTERN) < filtersToBeApplied_dict['reportPeriod'][1]]


            if ("reportName" in filtersToBeApplied_dict.keys() and expectedResultSet_name == []) or ("reportType" in filtersToBeApplied_dict.keys() and expectedResultSet_type == []) or ("deliveredOn" in filtersToBeApplied_dict.keys() and expectedResultSet_delv == []) or ("reportPeriod" in filtersToBeApplied_dict.keys() and expectedResultSet_period == []):
                expectedResultSet = []
            else:
                expectedResultSet = list(set.intersection(*(set(x) for x in [expectedResultSet_name, expectedResultSet_type, expectedResultSet_delv, expectedResultSet_period] if x)))   ### it will ignore empty lists for finding intersection of lists


            expectedCount = len(expectedResultSet)


            click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
            filtersAppliedFromFilterPopup = ReportHelper.setReportFilter(setup, reportScreenInstance, k=k)
            reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
            isError(setup)
            tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
            tableMap_afterFilters = reportScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
            if str(tableMap_afterFilters['rows']) == MRXConstants.NODATA:
                actualCount = 0
                checkEqualAssert(True,str(tableMap_afterFilters['rows']) == MRXConstants.NODATA ,message='Filter applied on multiple columns sucessfully')
                checkEqualAssert(expectedCount, actualCount, message='Verify Table Data after applying Filter = ' + str(filtersToBeApplied_dict.items()) + ' :::  Before Filter = ' + str(tableMap_beforeFilters['rows']) + ' :::  After Filter = ' + str(tableMap_afterFilters['rows']))

            else:
                actualCount = len(tableMap_afterFilters['rows'])
                checkEqualAssert(True, len(tableMap_beforeFilters['rows']) >= len(tableMap_afterFilters['rows']),
                             message='Filter applied on multiple columns sucessfully')
                checkEqualAssert(expectedCount, actualCount, message='Verify Table Data after applying Filter = ' + str(filtersToBeApplied_dict.items()) + ' :::  Before Filter = ' + str(tableMap_beforeFilters['rows'].values()) + ' :::  After Filter = ' + str(tableMap_afterFilters['rows'].values()))

            ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'filterClearIcon')

        else:
            logger.info("Invalid Scenario given for testing filters! All filters empty!")



##################################  Verify Filter on Column "Report Name"

    k = 5  ##  ==> refers to Report Name Filter Scenario in mrx_userlevel_config.xml  under "reportFilter"
    reportName = str(global_filter[str(k)]['reportname']).strip()

    if reportName != "":
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column1_ValuesFromTable_beforeFilters = reportScreenInstance.table.getColumnValueFromTable(1, tableHandle)
        expectedCount = column1_ValuesFromTable_beforeFilters.count(reportName)


        click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
        filtersAppliedFromFilterPopup = ReportHelper.setReportFilter(setup, reportScreenInstance, k=k)
        reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
        isError(setup)
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column1_ValuesFromTable_afterFilters = reportScreenInstance.table.getColumnValueFromTable(1, tableHandle)
        actualCount = len(column1_ValuesFromTable_afterFilters)


        checkEqualAssert(True, len(column1_ValuesFromTable_beforeFilters) >= len(column1_ValuesFromTable_afterFilters),message='Filter applied on column "Report Name" sucessfully')
        checkEqualAssert(expectedCount, actualCount,message='Verify Table Data after applying Filter on Report Name = ' + reportName + ' :::  Before Filter = ' + str(column1_ValuesFromTable_beforeFilters) + ' :::  After Filter = ' + str(column1_ValuesFromTable_afterFilters))
        ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'filterClearIcon')

    else :
        logger.info("Invalid Scenario given for testing filter on reportName")


#################################  Verify Filter on Column "Report Type"


    k = 6  ##  ==> refers to Report type Filter Scenario in mrx_userlevel_config.xml  under "reportFilter"
    reportType = str(global_filter[str(k)]['reporttype']).strip()

    if reportType  != "":
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column2_ValuesFromTable_beforeFilters = reportScreenInstance.table.getColumnValueFromTable(2, tableHandle)
        expectedCount = column2_ValuesFromTable_beforeFilters.count(reportType)

        click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
        filtersAppliedFromFilterPopup = ReportHelper.setReportFilter(setup, reportScreenInstance, k=k)
        reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
        isError(setup)
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column2_ValuesFromTable_afterFilters = reportScreenInstance.table.getColumnValueFromTable(2, tableHandle)
        actualCount = len(column2_ValuesFromTable_afterFilters)

        checkEqualAssert(True, len(column2_ValuesFromTable_beforeFilters) >= len(column2_ValuesFromTable_afterFilters),message='Filter applied on column "Report Type" sucessfully')
        checkEqualAssert(expectedCount, actualCount,message='Verify Table Data after applying Filter on Report Type = ' + reportType + ' :::  Before Filter = ' + str(column2_ValuesFromTable_beforeFilters) + ' :::  After Filter = ' + str(column2_ValuesFromTable_afterFilters))
        ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'filterClearIcon')

    else:
        logger.info("Invalid Scenario given for testing filter on reportType")


##############################  Verify Filter on Column "Delivererd on"

    k = 7  ##  ==> refers to Delievered on Filter Scenario in mrx_userlevel_config.xml  under "reportFilter"
    deliveredOnDropDownVal, deliveredOnDate = str(global_filter[str(k)]['deliveredon']).split("::")

    if deliveredOnDropDownVal != "" and deliveredOnDate != "":
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column3_valuesFromTable_beforeFilters = reportScreenInstance.table.getColumnValueFromTable(3, tableHandle)
        column3_epochValuesFromTable_beforeFilters = [getepoch(str(value), MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN) for value  in column3_valuesFromTable_beforeFilters]


        expectedResultSet = []
        if deliveredOnDropDownVal == "0":
            deliveredOnValFromDropDown = "After"
            validEpochStartTime = getepoch(str(deliveredOnDate), MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M")
            expectedResultSet = [epochValue for epochValue in column3_epochValuesFromTable_beforeFilters if epochValue >= validEpochStartTime]

        elif deliveredOnDropDownVal == "1":
            deliveredOnValFromDropDown = "Before"
            validEpochEndTime = getepoch(str(deliveredOnDate), MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M")
            expectedResultSet = [epochValue for epochValue in column3_epochValuesFromTable_beforeFilters if epochValue < validEpochEndTime]

        expectedCount = len(expectedResultSet)


        click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
        filtersAppliedFromFilterPopup = ReportHelper.setReportFilter(setup, reportScreenInstance, k=k)
        reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
        isError(setup)
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column3_valuesFromTable_afterFilters = reportScreenInstance.table.getColumnValueFromTable(3, tableHandle)
        actualCount = len(column3_valuesFromTable_afterFilters)

        checkEqualAssert(True, len(column3_valuesFromTable_beforeFilters) >= len(column3_valuesFromTable_afterFilters),message='Filter applied on column "Delivered on" sucessfully')
        checkEqualAssert(expectedCount, actualCount,message='Verify Table Data after applying Filter on Delivered on = ' + deliveredOnValFromDropDown + ' ' + deliveredOnDate + '    :::  Before Filter = ' + str(column3_valuesFromTable_beforeFilters) + ' :::  After Filter = ' + str(column3_valuesFromTable_afterFilters), testcase_id='MKR-3636')
        ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'filterClearIcon')

    else:
        logger.info("Invalid Scenario given for testing filter on Delivered On")



##############################  Verify Filter on Column " Report Period"

    k = 8  ##  ==> refers to Report Period Filter Scenario in mrx_userlevel_config.xml  under "reportFilter"
    ReportPeriodStartDate, ReportPeriodEndDate = str(global_filter[str(k)]['reportperiod']).split("::")

    if ReportPeriodStartDate != ""  and ReportPeriodEndDate != "":
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column4_valuesFromTable_beforeFilters = reportScreenInstance.table.getColumnValueFromTable(4, tableHandle)
        column4_epochValuesFromTable_beforeFilters = [(getepoch(str(value.split('-')[0].strip()), MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN),getepoch(str(value.split('-')[1].strip()), MRXConstants.TIMEZONEOFFSET, MRXConstants.TIMEPATTERN)) for value in column4_valuesFromTable_beforeFilters]


        expectedResultSet = []
        validEpochStartTime = getepoch(str(ReportPeriodStartDate), MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M")
        validEpochEndTime = getepoch(str(ReportPeriodEndDate), MRXConstants.TIMEZONEOFFSET, "%Y %B %d %H %M")
        expectedResultSet = [epochPair for epochPair in column4_epochValuesFromTable_beforeFilters if epochPair[0]  >= validEpochStartTime and epochPair[1] < validEpochEndTime]

        expectedCount = len(expectedResultSet)

        click_status = ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'nofilterIcon')
        filtersAppliedFromFilterPopup = ReportHelper.setReportFilter(setup, reportScreenInstance, k=k)
        reportScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
        isError(setup)
        tableHandle = getHandle(setup, MRXConstants.REPORTSCREEN, 'table')
        column4_valuesFromTable_afterFilters = reportScreenInstance.table.getColumnValueFromTable(4, tableHandle)

        actualCount = len(column4_valuesFromTable_afterFilters)

        checkEqualAssert(True, len(column4_valuesFromTable_beforeFilters) >= len(column4_valuesFromTable_afterFilters),message='Filter applied on column "Report Period" sucessfully')
        checkEqualAssert(expectedCount, actualCount,message='Verify Table Data after applying Filter on Report Period = ' + ReportPeriodStartDate  + ' - ' + ReportPeriodEndDate + '    :::  Before Filter = ' + str(column4_valuesFromTable_beforeFilters) + ' :::  After Filter = ' + str(column4_valuesFromTable_afterFilters))
        ReportHelper.clickOnfilterIcon(setup, MRXConstants.REPORTSCREEN, 'filterClearIcon')

    else:
        logger.info("Invalid Scenario given for testing filter on Report Period")




    setup.d.close()



except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()
