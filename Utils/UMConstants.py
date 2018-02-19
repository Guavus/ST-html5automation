from Utils.Constants import *
class UMConstants(Constants):
    UMSCREEN_MANAGEROLES = 'roleManagement_Screen'
    UMSCREEN_MANAGEUSERS = 'userManagement_Screen'
    UMScreenTableHeaderList_ManageUsers = ['Name', 'Username', 'Email', 'Application Role', 'Application Privileges','Network Role','Device Role', 'Last Modified', 'Status', 'Edit', 'Delete']
    UMScreenTableHeaderList_ManageRoles = ['Role Name','Default Privileges','Edit','Delete']
    NewRole = "New Application Role"
    UMPOPUP_ADDROLE = 'newRolePopUp_Screen'
    UMPOPUP_ADDUSER = 'newUserPopUp_Screen'
    UMPOPUP_DELETEROLE = "deletePopUp_Screen"
    UMHeader = "User Management"
    ExpectedOptionForNewRole = ['Role Name*', 'Application Privileges*']
    ExpectedOptionForNewUser = ['Username*', 'First Name*', 'Last Name*', 'Email*', 'Password*', 'Confirm Password*',
                                'User Image', 'Role*', 'Network Data Privileges', 'Device Data Privileges', 'Timezone*']

    RequiredFieldsLabel = "* required fields"
    RoleExistsLabel = "Role already exists"



