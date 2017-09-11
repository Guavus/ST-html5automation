from Utils.SetUp import *
from Utils.utility import *
from classes.Components.QuickTrendsComponentClass import *
import random
try:
    setup = SetUp()
    trendInstance=QuickTrendsComponentClass()
    h=getHandle(setup,"StackBarDummy_Screen","trend-main")

    setup.d.execute_script("return arguments[0].scrollIntoView();", h['trend-main']['trendchart'][0])
    paths=trendInstance.getColorFromBar_DCT(getHandle(setup,"StackBarDummy_Screen","trend-main"))

    trendInstance.hoverOverTicksGetMainBarChartText_DCT(setup,h,"StackBarDummy_Screen")

except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
