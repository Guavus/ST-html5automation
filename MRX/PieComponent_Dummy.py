from Utils.SetUp import *
from Utils.utility import *
from classes.Components.PieComponentClass import *
import random


try:
    setup = SetUp()
    PieInstance=PieComponentClass()
    pie = getHandle(setup,'Dummy_Screen', "piechart")
    pielegend= getHandle(setup, 'Dummy_Screen',"pielegend")

    data=PieInstance.getToolTipInfo(setup, setup.dH, getHandle(setup,'Dummy_Screen',"piechart"))
    PieInstance.setSelection(2,getHandle(setup,'Dummy_Screen', "piechart"),force=True)


except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
