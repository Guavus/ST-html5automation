from MuralUtils.ContentHelper import *
from MRXUtils import MRX_UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *
from classes.Pages.ExplorePageClass import *
from MRXUtils.MRXConstants import *

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    userScreenInstance = UserManagementScreenClass(setup.d)

    usersDetails = setup.cM.getNodeElements("changePassword_NegativeScenario", "user")
    clickOnProfileIconFlag = True

    for k, usersDetail in usersDetails.iteritems():
        exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
        exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),MuralConstants.Logout)
        login(setup, usersDetail['username'], usersDetail['password'])
        isError(setup)

        exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
        clickFlag = exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MRXConstants.ChangePassword)
        change_password_screen_handle = getHandle(setup, MRXConstants.ChangePasswordScreen)
        errorMsg, flag = MRX_UMHelper.ChangePassword(setup, userScreenInstance, MRXConstants.ChangePasswordScreen,change_password_screen_handle, usersDetail, button="Change")
        if flag:
            logger.error("Change Password should not be successful for User = %s CurrentPassword =%s NewPassword =%s ConfirmPassword =%s",str(usersDetail['username']),str(usersDetail['currentpassword']),str(usersDetail['newpassword']),str(usersDetail['newcpassword']))
            resultlogger.error("Change Password should not be successful for User = %s CurrentPassword =%s NewPassword =%s ConfirmPassword =%s <br>",str(usersDetail['username']),str(usersDetail['currentpassword']),str(usersDetail['newpassword']),str(usersDetail['newcpassword']))

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()