from Utils.Constants import *
class UMConstants(Constants):
    UMSCREEN_MANAGEROLES = 'roleManagement_Screen'
    UMSCREEN_MANAGEUSERS = 'userManagement_Screen'
    #UMScreenTableHeaderList_ManageUsers = ['Name', 'Username', 'Email', 'Application Role', 'Application Privileges','Network Role','Device Role', 'Last Modified', 'Status', 'Edit', 'Delete']
    UMSCREENTABLEHEADERLIST_MANAGEROLES = ['Role Name','Privileges','Edit','Delete']
    NEWROLE = "New Application Role"
    UMPOPUP_ADDROLE = 'newRolePopUp_Screen'
    UMPOPUP_ADDUSER = 'newUserPopUp_Screen'
    UMPOPUP_CONFIRM_DELETEROLE = "deletePopUp_Screen"
    UMPOPUP_ERROR = "errorPopup_Screen"
    UMHEADER = "User Management"
    EXPECTEDOPTIONFIELDS_ON_ADDROLEPOPUP = ['Role Name*', 'Application Privileges*']
    #EXPECTEDOPTIONFIELDS_ON_ADDUSERPOPUP = ['Username*', 'First Name*', 'Last Name*', 'Email*', 'Password*', 'Confirm Password*','User Image', 'Role*', 'Network Data Privileges', 'Device Data Privileges', 'Timezone*']

    REQUIREDFIELDSLABEL = "* required fields"
    ROLE_EXISTS_ERROR_MSG = "Role already exists"
    SAME_USER_ERROR_MSG = 'Username already exists.'
    LOGIN_ACCESSDENIED_MSG = 'Access denied, please contact administrator.'
    ROLE_IN_USE_MSG = "Role is already in use"
    SESSION_EXPIRED_MSG = "Session expired. Login again."
    ROLE_EXPIRED_MSG = "Role no more exists."
    AVAILABLE_PRIVILEGES = ['User Management','Export','Import','Workflow/UserDistribution','Workflow/DataExtraction']
    #ROLENAME_FORMAT = '[^A-Za-z0-9]' ## No special characters should be in the rolename
    MODIFIABLE_FIELDS_ALL = {"username":"disabled", "fname":"enabled", "lname":"enabled", "email":"enabled", "updatePasswordLink":"enabled", "password":"enabled", "cpassword":"enabled", "userrole":"enabled", "timezone":"enabled", "slider":"enabled"}
    MODIFIABLE_FIELDS_NO_PASS_ROLECHANGE_DISABLE = {"username":"disabled", "fname":"enabled", "lname":"enabled", "email":"enabled", "updatePasswordLink":"disabled", "password":"disabled", "cpassword":"disabled", "userrole":"disabled", "timezone":"enabled", "slider":"disabled"}

