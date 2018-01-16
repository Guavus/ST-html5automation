

from QuickTrendsComponentClass import QuickTrendsComponentClass
from Utils.logger import *
from selenium.webdriver import ActionChains
from MRXUtils.MRXConstants import *


class CBComponentClass(QuickTrendsComponentClass):
    def __init__(self):
        QuickTrendsComponentClass.__init__(self)
        self.util = __import__("Utils.utility")


    def hoverOverTicksGetMainHorizontalBarChartText(self,setup,h1,screenName,parent="trend-main",child="trendchart",tooltipParent="qttooltip",selectedCompareMes=""):
        try:
            totalbar, barHandle = self.getPointsOnHorizontalBarForHover_DCT(h1, parent=parent, child=child)
            yAxisPointList = self.getAxisPoint(self.util.utility.getHandle(setup, screenName,parent),child='yaxis')
            tooltipText = {}
            for index,el in enumerate(barHandle):
                if el=="None":
                    tooltipText[yAxisPointList[index]]=[]
                else:
                    setup.d.execute_script("return arguments[0].scrollIntoView();", el)
                    logger.info("Going to perform Hover Action")
                    time.sleep(2)
                    ActionChains(setup.d).move_to_element(el).perform()
                    flag,text=self.getTooltipTextAfterHover(setup,screenName,tooltipParent,selectedCompareMes=selectedCompareMes)
                    if not flag:
                        logger.info('Not able to Perform Hover Action')
                    else:
                        logger.info("Hover Action Performed")
                        for key in text.keys():
                            tooltipText[key]=text[key]

            logger.debug("Got tooltip data =  %s", str(tooltipText))
            return tooltipText

        except Exception as e:
            logger.error("Got Exception while performing hover actions = %s", str(e))
            return e

    def getAxisPoint(self,h, parent='trend-main', child='xaxis'):
        logger.info("Method Called : getAxisPoint")
        point = []
        if len(h[parent][child]) > 0:
            for ele in h[parent][child][0].find_elements_by_class_name('tick'):
                point.append(str(ele.text).strip())
        return point


    def  getTooltipTextAfterHover(self,setup,screenName,tooltipParent,child="dim_name",selectedCompareMes=""):
        flag=False
        toolTipText={}
        tooltipHandle=self.util.utility.getHandle(setup,screenName,tooltipParent)

        try:
            if len(tooltipHandle[tooltipParent][child])>0:
                flag=True
                dim=str(tooltipHandle[tooltipParent][child][0].text).split('\n')[0]
                valueArray=str(tooltipHandle[tooltipParent][child][0].text).split('\n')


                toolTipText[dim]=[]
                if selectedCompareMes in MRXConstants.AggreagableMeasureOnCB:
                    if len(tooltipHandle[tooltipParent]['color_Box']) == len(valueArray) - 1:  # for Color on Tooltip
                        for i in range(len(tooltipHandle[tooltipParent]['color_Box'])):
                            toolTipText[dim].append([self.rgb_to_hex(
                                tooltipHandle[tooltipParent]['color_Box'][i].value_of_css_property('background-color')),
                                                     valueArray[i + 1]])
                else:
                    if len(tooltipHandle[tooltipParent]['color_Box']) == len(valueArray) - 3:  # for Color on Tooltip
                        for i in range(len(tooltipHandle[tooltipParent]['color_Box'])):
                            toolTipText[dim].append([self.rgb_to_hex(
                                tooltipHandle[tooltipParent]['color_Box'][i].value_of_css_property('background-color')),valueArray[i + 2]])


                logger.info("Tootltip found with value = %s",str(toolTipText))
            else:
               logger.error("Tooltip Not Found :: Check Manually")

        except Exception as e:
            logger.error("Got Exception while getting value of Tooltip =%s",str(e))

        return flag,toolTipText