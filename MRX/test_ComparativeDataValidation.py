from Utils.SetUp import *
from classes.Pages.MRXScreens.ComparativeClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import CBHelper
from MRXUtils import SegmentHelper
from MRXUtils import UDHelper
from Utils.AvailableMethod import *
import json




def measureAndDimensionAfterMapping(timeRangeFromScreen, compareDimensionFromScreen, measureFromScreen, breakdownDimensionFromScreen, screenTooltipData={},filtersAppliedFlag=False):
    query = {}


    query['compare_dimension'] = []
    compareDimensions = ConfigManager().getNodeElements("compareDim_Mapping", "dimension")
    for k, compareDim in compareDimensions.iteritems():
        if str(k) == str(compareDimensionFromScreen):
            query['compare_dimension'].append(compareDim['backEnd_ID'])

    query['measure'] = []
    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    for k, measure in measures.iteritems():
        if str(k) == str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])

    query['breakdown_dimension'] = []
    breakdownDimensions = ConfigManager().getNodeElements("brokendownDim_Mapping", "dimension")
    for k, breakdownDim in breakdownDimensions.iteritems():
        if str(k) == str(breakdownDimensionFromScreen):
            query['breakdown_dimension'].append(breakdownDim['backEnd_ID'])

    if filtersAppliedFlag:
        filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
        for k, filter in filters.iteritems():
            if str(k) in screenTooltipData.keys() and screenTooltipData[k] != [] and str(screenTooltipData[k][0]).lower() != 'ALL'.lower():
                query[filter['backEnd_ID']] = screenTooltipData[k]

    timeRange = timeRangeFromScreen.split(Constants.TimeRangeSpliter)

    if len(timeRange) == 1:
        startTime = str(str(timeRange[0]).strip().split('(')[0]).strip() + " 00:00"
        query['starttime'] = str(getepoch(startTime, tOffset=MRXConstants.TIMEZONEOFFSET))
        query['endtime'] = str(getepoch(startTime, tOffset=MRXConstants.TIMEZONEOFFSET) + 86400)
    else:

        if len(str(timeRange[0]).strip().split(' ')) == 3:
            #query['starttime'] = str(getepoch(str(timeRange[0]).strip() + " 00:00", tOffset=MRXConstants.TIMEZONEOFFSET))
            query['starttime'] = '1509580800'
        else:
            query['starttime'] = str(getepoch(str(timeRange[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))

        if len(str(str(timeRange[1]).strip().split('(')[0]).strip().split(' ')) == 3:
            #query['endtime'] = str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip() + " 00:00",tOffset=MRXConstants.TIMEZONEOFFSET) + 86400)
            query['endtime'] = '1509926400'
        else:
            query['endtime'] = str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))

    query['count'] = 10

    return query





def fireBV(query,method,table_name,data,testcase=''):
    sleep(1)
    query['method']=method
    query['table_name']=table_name
    query['data']=data
    query['testcase']=testcase
    import time
    query['id']=str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(query))
    with open("CBDumpFile.txt",mode='a') as fs:
        fs.write(json.dumps(query))
        fs.write(" __DONE__" + "\n")





try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    cbScreenInstance =ComparativeClass(setup.d)

    cbScreenInstance.wfstart.launchScreen("Comparative", getHandle(setup, MRXConstants.WFSCREEN))


    ################################### Get all possible value for drop down from xml ##############################################

    compare_dim = setup.cM.getNodeElements("compare_dim", "dimension")
    compareDimList = []
    for k, compareDim in compare_dim.iteritems():
        compareDimList.append(compareDim['locatorText'])

    compare_mes = setup.cM.getNodeElements("compare_mes", "measure")
    compareMesList = []
    for k, compareMes in compare_mes.iteritems():
        compareMesList.append(compareMes['locatorText'])


    brokendown_dim = setup.cM.getNodeElements("brokendown_dim", "dimension")
    brokendownDimList = []
    for k, brokendownDim in brokendown_dim.iteritems():
        brokendownDimList.append(brokendownDim['locatorText'])




    ################################### CB Data Validation Scenarios for every (compare,measure,breakdown) combo #######################################################


    compareMethod_listFromXML = setup.cM.getNodeElements("testcaseMappingWithCompareMethod_CB", 'method')
    breakdownMethod_listFromXML = setup.cM.getNodeElements("testcaseMappingWithBreakdownMethod_CB", 'method')
    measure_listFromXML = setup.cM.getNodeElements("testcaseMappingWithMeasure_CB", 'measure')
    filter_listFromXML = setup.cM.getNodeElements("testcaseMappingWithFilters_CB", 'filter')
    quickLinks_listFromXML = setup.cM.getNodeElements("quickLinkTableTestCaseMapping_CB", 'quicklink')

    quickLink_list = quickLinks_listFromXML.keys()

    for ql in quickLink_list:
        ql = "Last 7 days"
        for cd in range(len(compareDimList)):
            compareFlag = True
            if compareDimList[cd] == "Segment":
                continue
            compareDimList[cd] = "APN"
            for cm in range(len(compareMesList)):
                measureFlag = True
                compareMesList[cm] = "Volume (Upload)"
                for bd in range(len(brokendownDimList)):
                    breakdownFlag = True
                    brokendownDimList[bd] = "Category"

                    timeRangeFromScreen, comDimBeforeApplyFilter, measureBeforeApplyFilter, breakdownDimBeforeApplyFilter = CBHelper.setQuickLink_Compare_Measure_BreakDown_forDV(setup, cbScreenInstance, ql, compareDimList[cd], compareMesList[cm], brokendownDimList[bd])
                    time.sleep(MRXConstants.SleepForComparativeScreen)
                    chartHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main')
                    chartData = cbScreenInstance.trend.hoverOverTicksGetMainHorizontalBarChartText(setup, chartHandle,MRXConstants.COMPARATIVESCREEN)
                    tableData = cbScreenInstance.table.getTableData1WithColumnHavingColor(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'table'))
                    table_name = quickLinks_listFromXML[ql]['table']

                    if tableData['rows'] != Constants.NODATA and chartData != {}:
                        if compareFlag:        ##### Get data from chart only
                            testcase1 = compareMethod_listFromXML[comDimBeforeApplyFilter]['testcase']
                            testcase2 = quickLinks_listFromXML[ql]['testcase']
                            queryFromUI = {}
                            queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, comDimBeforeApplyFilter,measureBeforeApplyFilter,breakdownDimBeforeApplyFilter)
                            ###### Preparing data to be validated
                            queryFromUI['table_header'] = [str(queryFromUI['compare_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")", "count(*)","group_concat(" + str(queryFromUI['breakdown_dimension']).strip("['").strip("']") + ")"]
                            cd_data_fromChart = []
                            compareDimValuesList_byRank = sorted([comValue.split("(")[1].strip(")") for comValue in chartData.keys()])
                            for compValueRank in compareDimValuesList_byRank:  ### iterating over each bar
                                key = [s for s in chartData.keys() if compValueRank in s]
                                if len(key) == 1:
                                    key = str(key).strip("['").strip("']")
                                    compareDimValue = str(key.split("(Rank")[0]).strip()
                                    numberOfBreakdownValues_perBar = len(chartData[key])
                                    sumOfMeasureValues_perBar = 0
                                    breakDownValues = []
                                    for breakdownDimList in chartData[key]:
                                        valuesAfterColorColumn = breakdownDimList[1].split(' ')
                                        if 'GB' in valuesAfterColorColumn or 'MB' in valuesAfterColorColumn or 'KB'in valuesAfterColorColumn:
                                            breakDownValues += [" ".join(valuesAfterColorColumn[:-4])]
                                            sumOfMeasureValues_perBar += UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3])))
                                        elif 'B' in valuesAfterColorColumn:
                                            breakDownValues += [" ".join(valuesAfterColorColumn[:-4])]
                                            sumOfMeasureValues_perBar += int(valuesAfterColorColumn[-4])
                                        else:
                                            breakDownValues += [" ".join(valuesAfterColorColumn[:-3])]
                                            sumOfMeasureValues_perBar += int(valuesAfterColorColumn[-3])
                                    cd_data_fromChart += [[compareDimValue, str(sumOfMeasureValues_perBar), str(numberOfBreakdownValues_perBar),",".join(breakDownValues)]]
                                else:
                                    logger.info("Bug:  More than one bar have the same Rank Number: " + str(compValueRank))
                            fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, cd_data_fromChart, testcase=testcase1 + "," + testcase2)

                            '''
                            print  "cd_data"
                            for ele in cd_data_fromChart:
                                print str(ele) + "\n"
                            '''
                            compareFlag = False




                        if measureFlag:         ##### Get data from chart and table
                            testcase1 = measure_listFromXML[measureBeforeApplyFilter]['testcase']
                            testcase2 = quickLinks_listFromXML[ql]['testcase']
                            queryFromUI = {}
                            queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, comDimBeforeApplyFilter,measureBeforeApplyFilter,breakdownDimBeforeApplyFilter)
                            ###### Preparing data to be validated
                            m_data_fromChart = []
                            m_data_fromTable = []

                            queryFromUI['table_header'] = [str(queryFromUI['compare_dimension']).strip("['").strip("']")  ,  "sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")", "count(*)","group_concat(" + str(queryFromUI['breakdown_dimension']).strip("['").strip("']") + ")"]

                            compareDimValuesList_byRank = sorted([comValue.split("(")[1].strip(")") for comValue in chartData.keys()])
                            for compValueRank in compareDimValuesList_byRank:   ### iterating over each bar
                                key = [s for s in chartData.keys() if compValueRank in s]
                                if len(key) == 1:
                                    key = str(key).strip("['").strip("']")
                                    compareDimValue = str(key.split("(Rank")[0]).strip()
                                    numberOfBreakdownValues_perBar = len(chartData[key])
                                    sumOfMeasureValues_perBar = 0
                                    breakDownValues = []
                                    for breakdownDimList in chartData[key]:
                                        valuesAfterColorColumn = breakdownDimList[1].split(' ')
                                        if 'GB' in valuesAfterColorColumn or 'MB' in valuesAfterColorColumn or 'KB' in valuesAfterColorColumn:
                                            breakDownValues += [" ".join(valuesAfterColorColumn[:-4])]
                                            sumOfMeasureValues_perBar += UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3])))
                                        elif 'B' in valuesAfterColorColumn:
                                            breakDownValues += [" ".join(valuesAfterColorColumn[:-4])]
                                            sumOfMeasureValues_perBar += int(valuesAfterColorColumn[-4])
                                        else:
                                            breakDownValues += [" ".join(valuesAfterColorColumn[:-3])]
                                            sumOfMeasureValues_perBar += int(valuesAfterColorColumn[-3])
                                    m_data_fromChart += [[compareDimValue, str(sumOfMeasureValues_perBar), str(numberOfBreakdownValues_perBar),",".join(breakDownValues)]]

                                else:
                                    logger.info("Bug:  More than one bar have the same Rank Number: "+ str(compValueRank))
                            fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, m_data_fromChart, testcase=testcase1 + "," + testcase2)

                            queryFromUI['table_header'] = [str(queryFromUI['breakdown_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")"]
                            for row in tableData['rows']:
                                breakdownDimValue = row[1]
                                measureValue = UnitSystem().getRawValueFromUI(str(row[3]))
                                m_data_fromTable += [[breakdownDimValue, measureValue]]
                            fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, m_data_fromTable, testcase=testcase1 + "," + testcase2)
                            '''
                            print  "m_data_fromChart"
                            for ele in m_data_fromChart:
                                print str(ele) + "\n"
                            print  "m_data_fromTable"
                            for ele in m_data_fromTable:
                                print str(ele) + "\n"
                            '''
                            measureFlag = False



                        if breakdownFlag:            #### Get data from chart and table
                            testcase1 = breakdownMethod_listFromXML[breakdownDimBeforeApplyFilter]['testcase']
                            testcase2 = quickLinks_listFromXML[ql]['testcase']
                            queryFromUI = {}
                            queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, comDimBeforeApplyFilter,measureBeforeApplyFilter,breakdownDimBeforeApplyFilter)
                            ###### Preparing data to be validated
                            bd_data_fromChart = []
                            bd_data_fromTable = []
                            queryFromUI['table_header'] = [str(queryFromUI['breakdown_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")", "count(*)", "group_concat(" + str(queryFromUI['compare_dimension']).strip("['").strip("']") + ")"]

                            sumOfMeasureValues_perBreakdownDim = {}
                            compareValuesCount_perBreakdown = 1
                            compareDimValuesList_byRank = sorted([comValue.split("(")[1].strip(")") for comValue in chartData.keys()])
                            for compValueRank in compareDimValuesList_byRank:
                                key = [s for s in chartData.keys() if compValueRank in s]
                                if len(key) == 1:
                                    key = str(key).strip("['").strip("']")
                                    compareDimValue = str(key.split("(Rank")[0]).strip()
                                    for breakdownDimList in chartData[key]:
                                        valuesAfterColorColumn = breakdownDimList[1].split(' ')
                                        if 'GB' in valuesAfterColorColumn or 'MB' in valuesAfterColorColumn or 'KB' in valuesAfterColorColumn:
                                            breakDownKey = " ".join(valuesAfterColorColumn[:-4])
                                            if breakDownKey in sumOfMeasureValues_perBreakdownDim.keys():
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][1] += 1
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][2] += "," + compareDimValue
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][0] += UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3])))
                                            else:
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey] = [UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3]))) , compareValuesCount_perBreakdown, compareDimValue]
                                        elif 'B' in valuesAfterColorColumn:
                                            breakDownKey = " ".join(valuesAfterColorColumn[:-4])
                                            if breakDownKey in sumOfMeasureValues_perBreakdownDim.keys():
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][1] += 1
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][2] += "," + compareDimValue
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][0] += int(valuesAfterColorColumn[-4])
                                            else:
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey] = [int(valuesAfterColorColumn[-4]) , compareValuesCount_perBreakdown , compareDimValue]
                                        else:
                                            breakDownKey = " ".join(valuesAfterColorColumn[:-3])
                                            if breakDownKey in sumOfMeasureValues_perBreakdownDim.keys():
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][1] += 1
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][2] += "," + compareDimValue
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey][0] += int(valuesAfterColorColumn[-3])
                                            else:
                                                sumOfMeasureValues_perBreakdownDim[breakDownKey] = [int(valuesAfterColorColumn[-3]) , compareValuesCount_perBreakdown , compareDimValue]
                                else:
                                    logger.info("Bug:  More than one bar have the same Rank Number: " + str(compValueRank))


                            for key in sumOfMeasureValues_perBreakdownDim.keys():
                                bd_data_fromChart += [[key, str(sumOfMeasureValues_perBreakdownDim[key][0]),str(sumOfMeasureValues_perBreakdownDim[key][1]),str(sumOfMeasureValues_perBreakdownDim[key][2])]]
                            fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, bd_data_fromChart, testcase=testcase1 + "," + testcase2)

                            queryFromUI['table_header'] = [str(queryFromUI['breakdown_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")"]
                            for row in tableData['rows']:
                                breakdownDimValue = row[1]
                                measureValue = UnitSystem().getRawValueFromUI(str(row[3]))
                                bd_data_fromTable += [[breakdownDimValue, measureValue]]
                            fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, bd_data_fromTable, testcase=testcase1 + "," + testcase2)
                            '''
                            print  "bd_data_fromChart"
                            for ele in bd_data_fromChart:
                                print str(ele) + "\n"
                            print  "bd_data_fromTable"
                            for ele in bd_data_fromTable:
                                print str(ele) + "\n"
                            '''
                            breakdownFlag = False


                    ################################ Checking Filter Scenarios with data validation  for every combo of dimension,measure

                        for x in range(MRXConstants.NUMBEROFFILTERSCENARIOFORCB):
                            k = 'dataValidation_'+str(x)

                            SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
                            expectedFilters = {}
                            expectedFilters = UDHelper.setUDPFilters(cbScreenInstance, setup, str(k),screen=MRXConstants.COMPARATIVESCREEN)
                            actualtoggleState = UDHelper.getToggleStateForFilters(cbScreenInstance, setup, str(k),screen=MRXConstants.COMPARATIVESCREEN)
                            cbScreenInstance.hoverAndClickButton(setup,"Apply",getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
                            time.sleep(MRXConstants.SleepForComparativeScreen)
                            screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
                            filterFromScreenForDV = UDHelper.mapToggleStateWithSelectedFilter(screenTooltipData,actualtoggleState)
                            chartHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main')
                            chartData = cbScreenInstance.trend.hoverOverTicksGetMainHorizontalBarChartText(setup,chartHandle,MRXConstants.COMPARATIVESCREEN)
                            time.sleep(5)
                            tableData = cbScreenInstance.table.getTableData1WithColumnHavingColor(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'table'))
                            queryFromUI = {}
                            queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, comDimBeforeApplyFilter,measureBeforeApplyFilter,breakdownDimBeforeApplyFilter,screenTooltipData=screenTooltipData,filtersAppliedFlag=True)

                            if tableData['rows'] != Constants.NODATA and chartData != {}:
                                ################## Preparing data for Compare dimension and Measure Values from chart
                                cd_data_fromChart = []
                                queryFromUI['table_header'] = [str(queryFromUI['compare_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")", "count(*)","group_concat(" + str(queryFromUI['breakdown_dimension']).strip("['").strip("']") + ")"]
                                compareDimValuesList_byRank = sorted([comValue.split("(")[1].strip(")") for comValue in chartData.keys()])
                                for compValueRank in compareDimValuesList_byRank:  ### iterating over each bar
                                    key = [s for s in chartData.keys() if compValueRank in s]
                                    if len(key) == 1:
                                        key = str(key).strip("['").strip("']")
                                        compareDimValue = str(key.split("(Rank")[0]).strip()
                                        numberOfBreakdownValues_perBar = len(chartData[key])
                                        sumOfMeasureValues_perBar = 0
                                        breakDownValues = []
                                        for breakdownDimList in chartData[key]:
                                            valuesAfterColorColumn = breakdownDimList[1].split(' ')
                                            if 'GB' in valuesAfterColorColumn or 'MB' in valuesAfterColorColumn or 'KB' in valuesAfterColorColumn:
                                                breakDownValues += [" ".join(valuesAfterColorColumn[:-4])]
                                                sumOfMeasureValues_perBar += UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3])))
                                            elif 'B' in valuesAfterColorColumn:
                                                breakDownValues += [" ".join(valuesAfterColorColumn[:-4])]
                                                sumOfMeasureValues_perBar += int(valuesAfterColorColumn[-4])
                                            else:
                                                breakDownValues += [" ".join(valuesAfterColorColumn[:-3])]
                                                sumOfMeasureValues_perBar += int(valuesAfterColorColumn[-3])

                                        cd_data_fromChart += [[compareDimValue, str(sumOfMeasureValues_perBar),str(numberOfBreakdownValues_perBar), ",".join(breakDownValues)]]
                                    else:
                                        logger.info("Bug:  More than one bar have the same Rank Number: " + str(compValueRank))
                                fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, cd_data_fromChart,testcase='')

                                ################## Preparing data for Break Down Dimension and Measure Values from Table
                                m_data_fromTable=[]
                                queryFromUI['table_header'] = [str(queryFromUI['breakdown_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")"]
                                for row in tableData['rows']:
                                    breakdownDimValue = row[1]
                                    measureValue = UnitSystem().getRawValueFromUI(str(row[3]))
                                    m_data_fromTable += [[breakdownDimValue, measureValue]]
                                fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, m_data_fromTable,testcase='')

                            ################## Preparing data for BreakDown Values from Chart

                                bd_data_fromChart = []
                                queryFromUI['table_header'] = [str(queryFromUI['breakdown_dimension']).strip("['").strip("']"),"sum(" + str(queryFromUI['measure']).strip("['").strip("']") + ")", "count(*)","group_concat(" + str(queryFromUI['compare_dimension']).strip("['").strip("']") + ")"]

                                sumOfMeasureValues_perBreakdownDim = {}
                                compareValuesCount_perBreakdown = 1
                                compareDimValuesList_byRank = sorted([comValue.split("(")[1].strip(")") for comValue in chartData.keys()])
                                for compValueRank in compareDimValuesList_byRank:
                                    key = [s for s in chartData.keys() if compValueRank in s]
                                    if len(key) == 1:
                                        key = str(key).strip("['").strip("']")
                                        compareDimValue = str(key.split("(Rank")[0]).strip()
                                        for breakdownDimList in chartData[key]:
                                            valuesAfterColorColumn = breakdownDimList[1].split(' ')
                                            if 'GB' in valuesAfterColorColumn or 'MB' in valuesAfterColorColumn or 'KB' in valuesAfterColorColumn:
                                                breakDownKey = " ".join(valuesAfterColorColumn[:-4])
                                                if breakDownKey in sumOfMeasureValues_perBreakdownDim.keys():
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][1] += 1
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][2] += "," + compareDimValue
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][0] += UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3])))
                                                else:
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey] = [UnitSystem().getRawValueFromUI(str(valuesAfterColorColumn[-4] + str(valuesAfterColorColumn[-3]))),compareValuesCount_perBreakdown, compareDimValue]
                                            elif 'B' in valuesAfterColorColumn:
                                                breakDownKey = " ".join(valuesAfterColorColumn[:-4])
                                                if breakDownKey in sumOfMeasureValues_perBreakdownDim.keys():
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][1] += 1
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][2] += "," + compareDimValue
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][0] += int(valuesAfterColorColumn[-4])
                                                else:
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey] = [int(valuesAfterColorColumn[-4]), compareValuesCount_perBreakdown,compareDimValue]
                                            else:
                                                breakDownKey = " ".join(valuesAfterColorColumn[:-3])
                                                if breakDownKey in sumOfMeasureValues_perBreakdownDim.keys():
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][1] += 1
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][2] += "," + compareDimValue
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey][0] += int(valuesAfterColorColumn[-3])
                                                else:
                                                    sumOfMeasureValues_perBreakdownDim[breakDownKey] = [int(valuesAfterColorColumn[-3]), compareValuesCount_perBreakdown,compareDimValue]


                                    else:
                                        logger.info("Bug:  More than one bar have the same Rank Number: " + str(compValueRank))
                                for key in sumOfMeasureValues_perBreakdownDim.keys():
                                    bd_data_fromChart += [[key, str(sumOfMeasureValues_perBreakdownDim[key][0]),str(sumOfMeasureValues_perBreakdownDim[key][1]),str(sumOfMeasureValues_perBreakdownDim[key][2])]]
                                fireBV(queryFromUI, AvailableMethod.Top_Row, table_name, bd_data_fromChart,testcase='')

                                print ("Done")
                            break   ## -------- come out from filter scenarios loop
                        break
                    break
                break
            break




except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()