from Utils.SetUp import *
from classes.Pages.MRXScreens.ComparativeClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from classes.Components.WorkflowStartComponent import *
from MRXUtils import CBHelper
from MRXUtils import SegmentHelper
from MRXUtils import UDHelper

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle, "WORKFLOWS")
    cbScreenInstance =ComparativeClass(setup.d)

    UD_Flag=cbScreenInstance.wfstart.launchScreen("Comparative", getHandle(setup, MRXConstants.WFSCREEN))
    checkEqualAssert(True,UD_Flag,message="Verify that user can open the Comparative breakdown Screen from the Workflows tab",testcase_id='MKR-3534')



    ####################### Get all possible value for drop down from xml ##############################################

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

    '''
    ######################################## Default values on CB Screen ################################################
    defaultSelectionOnScreen=[]
    defaultQuicklink = cbScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "ktrs"))
    defaultSelectionOnScreen.append(defaultQuicklink)

    defaultCompareDim = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"),index=0)
    defaultSelectionOnScreen.append(defaultCompareDim)

    defaultCompareMes = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), index=1)
    defaultSelectionOnScreen.append(defaultCompareMes)

    defaultBrokenDown = cbScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), index=2)
    defaultSelectionOnScreen.append(defaultBrokenDown)

    defaultChartHeader = CBHelper.getChartLegendheaders(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'chart_legend_headers'))
    defaultSelectionOnScreen.append(defaultChartHeader)

    defaultLegendHeader = CBHelper.getChartLegendheaders(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'chart_legend_headers'),child='text_over_legend')
    defaultSelectionOnScreen.append(defaultLegendHeader)

    defaultInitalMsgOnChart = CBHelper.getMsgOnNoData(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'cb_no_data_msg'))
    defaultSelectionOnScreen.append(defaultInitalMsgOnChart)

    defaultInitalMsgOnLegend = CBHelper.getMsgOnNoData(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'cb_no_data_msg'),child='msgOnLegend')
    defaultSelectionOnScreen.append(defaultInitalMsgOnLegend)

    checkEqualAssert(MRXConstants.DefaultSelectionOnCBScreen,defaultSelectionOnScreen,message="Verify the default values of the Comparative breakdown Screen from the Workflows tab",testcase_id="MKR-3536,3508")

    ######################################### Available Quicklinks on CB screen ###########################################################################

    actualAvailableQuickLinkList = UDHelper.availableQuickLink(setup, MRXConstants.COMPARATIVESCREEN)
    checkEqualAssert(MRXConstants.ExpectedQuickLinkList, actualAvailableQuickLinkList,message='Verify that avalivale quicklinks on CB screen are: "Last 6 Months", "Last Month", "Last 7 days", "Yesterday", "Today", "Calender"',testcase_id='')

    ############################################## Avalibale Options in dropdowns on CB screen #############################################################

    h=getHandle(setup,MRXConstants.COMPARATIVESCREEN,'allselects')
    compare=cbScreenInstance.dropdown.availableDropDownOption(h,index=0)
    by=cbScreenInstance.dropdown.availableDropDownOption(h,index=1)
    brokenDown=cbScreenInstance.dropdown.availableDropDownOption(h,index=2)

    checkEqualAssert(MRXConstants.ExpectedCompareValue,compare,message="Verify available option for 'Compare' drop down",testcase_id="MKR-3539,3542")
    checkEqualAssert(MRXConstants.ExpectedMeasureOnCB,by,message="Verify available option for Measure",testcase_id="MKR-3543")
    checkEqualAssert(MRXConstants.ExpectedBrokenDownValue,brokenDown,message="Verify available option for 'Broken down by'  drop down",testcase_id="MKR-3546,3542")

    cbScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "breadcrumb"))
    workFlowOption = cbScreenInstance.cm.availableOptionOnWorkFlowDrop(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "breadcrumb"))
    checkEqualAssert(MRXConstants.ExpectedOptionForWorkFlow,workFlowOption,message="Verify available option for workflows drop down menu",testcase_id="MKR-3540")
    '''
    ###################################### Match Color sequence in bar and table, Table data order(Measure) should be Desc   ##################################################

    quickLinks_listFromXML = setup.cM.getNodeElements("quickLinkTableTestCaseMapping_CB", 'quicklink')

    quickLink_list = quickLinks_listFromXML.keys()

    for ql in quickLink_list:
        ql = "Last 7 days"
        for cd in range(len(compareDimList)):
            selectedCompareDim = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(compareDimList[cd]), index=0, parent="allselects")
            isError(setup)
            for cm in range(len(compareMesList)):
                selectedCompareMes = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(compareMesList[cm]), index=1,parent="allselects")
                isError(setup)
                for bd in range(len(brokendownDimList)):
                    selectedBrokenDown = cbScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.COMPARATIVESCREEN, "allselects"), str(brokendownDimList[bd]), index=2,parent="allselects")
                    isError(setup)
                    sleep(MRXConstants.SleepForComparativeScreen)
                    tableData=cbScreenInstance.table.getTableData1WithColumnHavingColor(getHandle(setup, MRXConstants.COMPARATIVESCREEN,'table'))
                    chartHandle = getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main')
                    chartData = cbScreenInstance.trend.hoverOverTicksGetMainHorizontalBarChartText(setup, chartHandle,MRXConstants.COMPARATIVESCREEN)

                    if tableData['rows']!=Constants.NODATA and chartData!={}:
                        CBHelper.validateSortingInTable(cbScreenInstance,tableData,"",selectedCompareMes)
                        color_List=cbScreenInstance.trend.getAllColorOnHorizontalBar_DCT(setup,chartHandle)
                        yAxisPointList = CBHelper.getAxisPoint(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main'), child='yaxis')
                        barColorDict = CBHelper.map_YAxisWithColorList(yAxisPointList,color_List)
                        flag=CBHelper.validateColorSequence(barColorDict,tableData)
                        checkEqualAssert(True,flag,message="Verify the colour sequence of the table and bar",testcase_id="MKR-3563")
                        flag=CBHelper.validateColorOnTooltipWithBar(chartData,barColorDict)

                    elif tableData['rows']== Constants.NODATA:
                        msg1 = CBHelper.getNoDataMsg(setup, MRXConstants.COMPARATIVESCREEN, child='msgOnLegend')
                        checkEqualAssert(MRXConstants.NODATAMSG, msg1,
                                     measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',
                                     testcase_id='')

                        r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                        setup.d.save_screenshot(r)
                        logger.debug("No Table Data for selected compare = %s, measure = %s,brokendownvalue = %s :: Screenshot with name = %s is saved"
                                 ,selectedCompareDim,selectedCompareMes,brokendownDimList, r)
                        resultlogger.info("No Table Data for selected compare = %s, measure = %s,brokendownvalue = %s :: Screenshot with name = %s is saved"
                                 ,selectedCompareDim,selectedCompareMes,brokendownDimList, r)


    setup.d.close()
    import MRX.test_Header
    import MRX.test_Footer

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


