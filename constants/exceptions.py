class ErrorMessages:

    # Client Error Messages
    DUPLICATE_EMAIL_IN_REGISTRATION = ("CRM_1001", "Duplicate email.", "Email should be unique.")
    INVALID_CONFIRMATION_TOKEN = ("CRM_1002", "Invalid confirmation token.", "")
    EXPIRED_INVITATION_TOKEN = ("CRM_50016", "Invitation has expired", "")
    USER_NOT_INVITED_TO_SIGNUP = ("CRM_1003", "Unauthorized user.", "User not invited to signup.")
    USER_ROLE_UNDEFINED = ("CRM_1003", "Undefined user role.", "Can't fine user role")
    EXISTING_USER_INVITATION = ("CRM_1004", "Already Existing User.",
                                "A user is already existing under the provided email.")
    EMPTY_USER_INVITATION = ("CRM_1005", "Empty Email Address.", "Email cannot be empty in invitation.")
    EXISTING_USER_SIGNUP = ("CRM_1006", "Already Existing User.",
                            "A user is already existing under the provided email.")
    ADMIN_SIGNUP_FAILED = ("CRM_1007", "Admin/Sales  agent signup failed.",
                           "An error occurred while signing up.")
    INVALID_ID_IN_ADMIN_UPDATE = ("CRM_1008", "No existing user.", "The provided user id does not exist")
    USER_ID_NOT_MATCH = ("CRM_1008", "Can't change other user's password.", "The provided user id does not exist")
    USER_PASSWORD_DOESNT_MATCH = ("CRM_1008", "User password doesnt match.", "")
    USER_NOT_EXISTING = ("CRM_1008", "User Not Existing ",
                         "User is not in the system.")
    # Content Error Messages
    EXISTING_ITEM = ("CRM_1008", "Already Existing Item",
                     "Item is already in the system.")
    EXISTING_COUNTRY = ("CRM_1008", "Already Existing Country",
                        "Country is already in the system.")
    COUNTRY_NOT_EXISTING = ("CRM_1008", "Country Not Existing ",
                            "Country is not in the system.")
    COUNTRY_ADD_FAILED = ("CRM_1009", "Country add fail",
                          "New country added fail.")
    STATE_ADD_FAILED = ("CRM_1010", "State add fail",
                        "New state added fail.")
    EXISTING_STATE = ("CRM_1011", "Already Existing State",
                      "State is already in the system.")
    STATE_NOT_EXISTING = ("CRM_1008", "State Not Existing ",
                          "State is not in the system.")
    CITY_ADD_FAILED = ("CRM_1012", "City add fail",
                       "New City added fail.")
    EXISTING_CITY = ("CRM_1013", "Already Existing City",
                     "City is already in the system.")
    EXISTING_ADS_ACCOUNT = ("CRM_1014", "Already Existing Ads Account",
                            "Ads Account is already in the system.")
    ADS_ACCOUNT_ADD_FAILED = ("CRM_1015", "Ads Account add fail",
                              "Company or agent not existing")

    # Server Error Messages
    INVITATION_EMAIL_SENDING_FAILED = ("CRM_4001", "Email sending failed.",
                                       "Problem occurred in sending the invitation.")
    RESET_EMAIL_SENDING_FAILED = ("CRM_4002", "Email sending failed.",
                                  "Problem occurred in sending the reset link.")
    INVITING_NEW_USER_FAILED = ("CRM_4003", "Inviting new user failed.",
                                "Problem occurred in adding a new admin/sales agent.")
    ADMIN_UPDATE_FAILED = ("CRM_4004", "Admin update failed.", "Problem occurred in updating new admin/sales agent.")
    TOKEN_VERIFICATION_IN_SIGNUP_FAILED = ("CRM_4005", "Token verification failed.",
                                           "Problem occurred in token verification.")
    ADDRESS_INPUT_FAILED = ("CRM_4006", "Address creation failed.", "Problem occurred in saving the address.")
    COMPANY_CREATION_FAILED = ("CRM_4007", "Company creation failed.", "Problem occurred in company creation")
    GET_COMPANY_LIST_FAILED = ("CRM_4008", "Get company list failed.", "Problem occurred in get company list")
    GET_COUNTRY_LIST_FAILED = ("CRM_4009", "Get country list failed.", "Problem occurred in get country list")
    GET_STATE_LIST_FAILED = ("CRM_4010", "Get state list failed.", "Problem occurred in get state list")
    GET_CITY_LIST_FAILED = ("CRM_4011", "Get city list failed.", "Problem occurred in get city list")
    GET_ADS_ACCOUNT_LIST_FAILED = (
        "CRM_4012", "Get Ads Account list failed.", "Problem occurred in get Ads account list")
    AGENT_NOT_FOUND = ("CRM_4012", "Agent does not exist.", "")
    MARKET_NOT_FOUND = ("CRM_4012", "Market does not exist.", "")

    # Authentication Error Messages
    INVALID_TOKEN = ("CRM_5001", "Invalid token", "")
    INVALID_USERNAME = ("CRM_5002", "Invalid username", "")
    INVALID_USERNAME_PASSWORD = ("CRM_5003", "Invalid username or password", "")
    INVALID_ROLE = ("CRM_5004", "Invalid role", "")
    EXPIRED_TOKEN = ("CRM_5005", "Signature has expired", "")
    BAD_RESET_TOKEN = ("CRM_5006", "Invalid reset token", "")

    EXPIRED_OTP = ("CRM_5007", "OTP has expired", "")
    BAD_OTP_TOKEN = ("CRM_5008", "Invalid OTP token", "")
    INVALID_USERNAME_OTP = ("CRM_5009", "Invalid username or OTP", "")
    INVALID_OTP = ("CRM_5010", "Invalid OTP", "")

    COMPANY_NOT_EXISTING = ("CRM_1008", "Company Not Existing ",
                            "Company is not in the system.")

    # REGISTER_INVALID_PASSWORD = "REGISTER_INVALID_PASSWORD"
    #     REGISTER_USER_ALREADY_EXISTS = "REGISTER_USER_ALREADY_EXISTS"
    #     LOGIN_BAD_CREDENTIALS = "LOGIN_BAD_CREDENTIALS"
    #     LOGIN_USER_NOT_VERIFIED = "LOGIN_USER_NOT_VERIFIED"
    #     RESET_PASSWORD_BAD_TOKEN = "RESET_PASSWORD_BAD_TOKEN"
    #     RESET_PASSWORD_INVALID_PASSWORD = "RESET_PASSWORD_INVALID_PASSWORD"
    #     VERIFY_USER_BAD_TOKEN = "VERIFY_USER_BAD_TOKEN"
    #     VERIFY_USER_ALREADY_VERIFIED = "VERIFY_USER_ALREADY_VERIFIED"
    #     UPDATE_USER_EMAIL_ALREADY_EXISTS = "UPDATE_USER_EMAIL_ALREADY_EXIST
