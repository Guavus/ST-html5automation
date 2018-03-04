from MuralUtils.ContentHelper import *
from UMUtils import UMHelper
from classes.Pages.MuralScreens.RoleManagementScreen import *
from classes.Pages.ExplorePageClass import *
#from MRXUtils.MRXConstants import *
from UMUtils.UMConstants import *
from classes.Pages.MuralScreens.UserMangementScreen import UserManagementScreenClass

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    userScreenInstance = UserManagementScreenClass(setup.d)
    handle = getHandle(setup, "explore_Screen","alllabels")
    roleScreenInstance=RoleManagementScreenClass(setup.d)
    roleScreenInstance.click(handle['alllabels']['label'][1])



    ################# Verify session expire prompt on performing action on of the multiple logged in tabs and user logs out from one in the middle
    # body = setup.d.find_element_by_tag_name("body")
    # body.send_keys(Keys.COMMAND + 't')
    # setup.d.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    # setup.d.switch_to.window(setup.d.window_handles[1])
    # firsttab = setup.d.current_window_handle
    # setup.d.switch_to_window(firsttab)

    setup.d.execute_script("window.open('"+Constants.URL+"','_blank');")
    setup.d.switch_to.window(setup.d.window_handles[1])
    handle = getHandle(setup, "explore_Screen", "alllinks")
    userScreenInstance.click(handle['alllinks']['a'][0])  ## Click on Profile link
    handle = getHandle(setup, "explore_Screen", "alllinks")
    userScreenInstance.click(handle['alllinks']['a'][2])  ## Click on Logout
    time.sleep(5)

    setup.d.switch_to.window(setup.d.window_handles[0])
    handle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'newRoleIcon')
    click_status = UMHelper.clickOnPopupIcon(setup, h=handle, screen=UMConstants.UMSCREEN_MANAGEROLES,parent='newRoleIcon', child='icon')

    erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg', child='msg')
    checkEqualAssert(UMConstants.SESSION_EXPIRED_MSG, msgFromUI,message=" Verify that a session expire msg appears on all other tabs when same user is logged in multiple tabs of the same browser window and suddenly user logs out from one of the tabs.",testcase_id='Reflex-UM-199')

    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'allbuttons')
    roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
    time.sleep(5)
    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
    loginHandle = getHandle(setup,Constants.LOGINSCREEN)
    checkEqualAssert(str([0,True]), str([len(handle['ErrorMsg']['msg']), len(loginHandle['username']['username']) > 0]),message="Verify that on clicking on 'Ok' button, Session Expire Error Popup disappears and login page is rendered again",testcase_id='Reflex-UM-199')



    '''
    ################### Verify that a valid error popup appears on session timeout
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    handle = getHandle(setup, "explore_Screen", "alllabels")
    roleScreenInstance.click(handle['alllabels']['label'][1])
    isError(setup)
    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
    logging.info("Session expire popup, Start time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    setup.d.waitForVisibleElement(locator="p.gvs-alert-message", wait=True, isParent=False)
    logging.info("Session expire popup, End time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg', child='msg')
    checkEqualAssert(UMConstants.SESSION_EXPIRED_MSG, msgFromUI, message="Verify that a valid error popup appears on session timeout ",testcase_id='Reflex-UM-198')

    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'allbuttons')
    roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
    time.sleep(5)
    handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
    loginHandle = getHandle(setup, Constants.LOGINSCREEN)
    checkEqualAssert(str([0, True]),str([len(handle['ErrorMsg']['msg']), len(loginHandle['username']['username']) > 0]),message="Verify that on clicking on 'Ok' button, Session Expire Error Popup disappears and login page is rendered again",testcase_id='Reflex-UM-198')

    '''



    ################### Verify handling for disable delete /edit icons under Manage Roles table
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    handle = getHandle(setup, "explore_Screen", "alllabels")
    roleScreenInstance.click(handle['alllabels']['label'][0])
    elem_edit = setup.d.find_element_by_css_selector("span.iconStyleDisable.userActionEdit")
    setup.d.execute_script("arguments[0].style.opacity = 1", elem_edit)
    edit_click_status = userScreenInstance.click(elem_edit)
    if edit_click_status != True:
        edit_click_status = False
    checkEqualAssert(False, edit_click_status,message="Verify that edit button is not clickable even after it is enabled by some malacious user.",testcase_id='Reflex-UM-254')

    elem_delete = setup.d.find_element_by_css_selector("span.iconStyleDisable.userActionDelete")
    setup.d.execute_script("arguments[0].style.opacity = 1", elem_delete)
    delete_click_status = userScreenInstance.click(elem_delete)
    if delete_click_status != True:
        delete_click_status = False
    checkEqualAssert(False, delete_click_status,message="Verify that delete button is not clickable even after it is enabled by some malacious user.",testcase_id='Reflex-UM-254')
    '''
    ********************************************** For ROles
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    handle = getHandle(setup, "explore_Screen", "alllabels")
    roleScreenInstance.click(handle['alllabels']['label'][1])
    elem_edit = setup.d.find_element_by_css_selector("span.iconStyleDisable.roleActionEdit")
    setup.d.execute_script("arguments[0].style.opacity = 1", elem_edit)
    edit_click_status = userScreenInstance.click(elem_edit)
    if edit_click_status != True:
        edit_click_status = False
    checkEqualAssert(False, edit_click_status,message="Verify that edit button is not clickable even after it is enabled by some malacious user.",testcase_id='Reflex-UM-254')

    elem_delete = setup.d.find_element_by_css_selector("span.iconStyleDisable.roleActionDelete")
    setup.d.execute_script("arguments[0].style.opacity = 1", elem_delete)
    delete_click_status = userScreenInstance.click(elem_delete)
    if delete_click_status != True:
        delete_click_status = False
    checkEqualAssert(False, delete_click_status,message="Verify that delete button is not clickable even after it is enabled by some malacious user.",testcase_id='Reflex-UM-254')

    '''

    ################## Verify the behaviour when superadmin tries to edit a user which has already been deleted by another admin user at the same time.
    handle = getHandle(setup, "explore_Screen", "alllabels")
    roleScreenInstance.click(handle['alllabels']['label'][1])
    userLoginDetailsForManageRolesDict = setup.cM.getNodeElements("umUserLoginDetailsForManageRoles", "user")
    setup1 = SetUp()
    login(setup1,userLoginDetailsForManageRolesDict['adminuser1']['username'] , userLoginDetailsForManageRolesDict['adminuser1']['password'])
    handle = getHandle(setup1, "explore_Screen", "alllabels")
    roleScreenInstance.click(handle['alllabels']['label'][1])
    tableHandle = getHandle(setup1, UMConstants.UMSCREEN_MANAGEROLES, 'table')
    column_ValuesFromTable = roleScreenInstance.table.getColumnValueFromTable(0, tableHandle)
    for value in column_ValuesFromTable:
        if value != "Admin":
            break
    logger.info("Deleting Role : " + str(value))
    try:
        click_status, delete_status, click_status_fromDelPopup, popup_disappear_status = UMHelper.deleteRole(setup=setup1, tableHandle=tableHandle,screenInstance=roleScreenInstance,columnValueInRowToBeDeleted=str(value),parentScreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_CONFIRM_DELETEROLE,colIndex=0)
    except Exception as e:
        logger.info("Got Exception on deleting role : " + str(value) + "  " + str(e))
        click_status, delete_status, click_status_fromDelPopup, popup_disappear_status = "", "", "", ""
    setup1.d.close()

    if popup_disappear_status == True:
        logger.info("Updating already deleted role : " + str(value))
        tableHandle = getHandle(setup, UMConstants.UMSCREEN_MANAGEROLES, 'table')
        try:
            click_status, expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = UMHelper.editRole(setup=setup, tableHandle=tableHandle,screenInstance=roleScreenInstance, columnValueInRowToBeEdited=str(value),roleDetail={'rolename':str(value),'applicationprivileges':'3'},parentscreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_ADDROLE,k='0', colIndex=0)
        except Exception as e:
            logger.info("Got Exception on updating role : " + str(value) + "  " + str(e))

    if updateBtnStatus == True:
        handle = getHandle(setup, UMConstants.UMPOPUP_ADDROLE, "allbuttons")
        roleScreenInstance.click(handle['allbuttons']['button'][0])
        erroFlag, msgFromUI = UMHelper.errorMsgOnPopUp(setup, UMConstants.UMPOPUP_ERROR, parent='ErrorMsg', child='msg')
        checkEqualAssert(UMConstants.ROLE_EXPIRED_MSG,str(msgFromUI),message="Verify that valid error messages appears when one admin user tries to edit another user that has been deleted by other admin user in the same login session.",testcase_id='Reflex-UM-')
        handle = getHandle(setup,UMConstants.UMPOPUP_ERROR,"allbuttons")
        roleScreenInstance.hoverAndClickButton(setup, "Ok", handle)
        time.sleep(5)
        handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, 'ErrorMsg')
        checkEqualAssert(0,len(handle['ErrorMsg']['msg']),message="Verify that on clicking on 'Ok' button,  Error Popup disappears",testcase_id='Reflex-UM-')

    setup.d.close()


except Exception as e:
    logger.debug("Exception Occurred: "+ str(e))
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()


