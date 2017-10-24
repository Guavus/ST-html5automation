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

    ####################### get all possible value for drop down from xml ##############################################

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



    checkLoadMore=True
    checkLoadMoreCount=0
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
                    checkLoadMore = CBHelper.expandMoreOnCB(setup, cbScreenInstance, MRXConstants.COMPARATIVESCREEN,child="load_more", checkLoadMore=checkLoadMore)
                    if not checkLoadMore and checkLoadMoreCount==0:
                        CBHelper.validateSortingInTable(cbScreenInstance,tableData,"",selectedCompareMes)
                        color_List=cbScreenInstance.trend.getAllColorOnHorizontalBar_DCT(setup,chartHandle)
                        yAxisPointList = CBHelper.getAxisPoint(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main'), child='yaxis')
                        barColorDict = CBHelper.map_YAxisWithColorList(yAxisPointList,color_List)
                        flag=CBHelper.validateColorSequence(barColorDict,tableData)
                        checkEqualAssert(True,flag,message="Verify the colour sequence of the table and bar with load more functionality",testcase_id="MKR-3563")
                        CBHelper.validateColorOnTooltipWithBar(chartData,barColorDict)
                        checkLoadMoreCount=checkLoadMoreCount+1

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.error("Got Exception : %s", str(e))
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


# xAxisPointList = CBHelper.getAxisPoint(getHandle(setup, MRXConstants.COMPARATIVESCREEN, 'trend-main'))
# if chartData=={}:
#     msg=CBHelper.getNoDataMsg(setup,MRXConstants.COMPARATIVESCREEN,child='msgOnChart')
# if tableData['rows']==Constants.NODATA:
#     msg1=CBHelper.getNoDataMsg(setup,MRXConstants.COMPARATIVESCREEN,child='msgOnLegend')

# chartHeader=CBHelper.getHeader(setup,MRXConstants.COMPARATIVESCREEN,parent='cb_chart_header')
# legendHeader = CBHelper.getHeader(setup, MRXConstants.COMPARATIVESCREEN, parent='cb_legend_header')
