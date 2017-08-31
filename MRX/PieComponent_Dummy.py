from Utils.SetUp import *
from Utils.utility import *
from classes.Components.PieComponentClass import *
from classes.Components.PieLegendComponentClass import *
import random
'''
This script cover testing of below method
1. Set selection on Pie Component
2. Get selection from Pie (Selected Index and data)
3. Get selection from PieLegend (Selected Index and data)
4. Get toolTip data ( By hover on Pie chart)
5. Get all date from table (with scrolling)
6. Set totalSelection on Pie

'''

try:
    setup = SetUp()
    PieInstance=PieComponentClass()
    PieLegendInstance=PieLegendComponentClass()
    pie = getHandle(setup,Constants.DUMMY_SCREEN, "piechart")
    pielegend= getHandle(setup,Constants.DUMMY_SCREEN,"pielegend")

    data=PieInstance.getToolTipInfo(setup, setup.dH, getHandle(setup,Constants.DUMMY_SCREEN,"piechart"))
    Pie_Selection=setup.cM.getNodeElements("PieSelection_Scenario","PieSelection")
    PieInstance.setSelection(int(Pie_Selection['0']['value']),getHandle(setup,Constants.DUMMY_SCREEN),force=True)

    i = PieInstance.getPieSelections(getHandle(setup, Constants.DUMMY_SCREEN,"piechart"))
    j = PieLegendInstance.getSelection(getHandle(setup,Constants.DUMMY_SCREEN,"pielegend"))
    r = PieLegendInstance.getData11(getHandle(setup,Constants.DUMMY_SCREEN,"pielegend"))

    # dim, value = str(r['legendText'][int(j['selIndices'][0])].split('\n')[0]), str(r['legendText'][int(j['selIndices'][0])].split('\n')[1])
    # checkEqualAssert(len(i), len(j['selIndices']), message="Verify Sync between Pie and PieLegend")

    Pie_text=PieInstance.getPieSelectionText(getHandle(setup,Constants.DUMMY_SCREEN, "piechart"))
    PieInstance.setTotalSelectionOnPie(getHandle(setup,Constants.DUMMY_SCREEN, "piechart"))

    # checkEqualAssert(Pie_text[0],dim,message="Verify Same Text on Pie and PieLegend")
    # checkEqualAssert(Pie_text[1],value,message="Verify Same value on Pie and PieLegend")
    pass
except Exception as e:
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
