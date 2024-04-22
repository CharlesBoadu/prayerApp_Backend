response_codes={
    "SUCCESS":"PA00",
    'INTERNAL_ERROR':'PA01',
    'BAD_REQUEST':'PA02',
    'ALREADY_EXIST':'PA03',
    'ADD_SUCCESS':'PA04',
    'SIGNUP_ERROR':'PA05',
    'NOT_FOUND':'PA06',
    'USER_DELETED' : 'PA07',
    'ERROR_DELETION': 'PA08',
    'DOES NOT EXIST':'PA09',
    'SUCCESSFULLY FETCHED':'PA09'
}

# **************** Custom Service Status Codes ****************
CODE_SUCCESS = "PA00"
CODE_FAILURE = "PA01"
CODE_TERMINATED_ACCOUNT = "PA05"
CODE_SERVICE_INTERNAL_ERROR = "PA02"
CODE_SERVICE_INTERNAL_ERROR_MISSING_PARAM = "PA03"
CODE_SERVICE_INTERNAL_ERROR_INVALID_ARGUMENT = "PA04"

# **************** Static text declaration ****************
en = {
    "APPLICATION": "DB_TEMPLATE.",
    "ACCOUNT_TERMINATED": "User Account Terminated.",
    "UNAUTHORIZED_ACCESS": "ACCESS DENIED.",
    "OPERATION_SUCCESSFUL": "Operation Successful.",
    "OPERATION_ERROR": "Error: {}",
    "ERROR_OCCURRED": "An error occurred:",
    "EMPTY_RESPONSE": "No data found.",
    "INVALID_ID": "ID is Invalid. No data found.",
    "INVALID_EMAIL": "Email ID is Invalid. No data found.",
    "MISSING_PARAMETER": "Missing Parameter: {}",
    "DUPLICATE_ENTRY": "Duplicate entry for '{}'",
    "SIGNING_SUCCESSFUL": "Signin Successful.",
    "SIGNING_FAILURE": "Wrong email or password.",
    "SIGNING_FAILURE_PASSWORD": "Wrong password.",
    "SIGNING_ACTIVITY_FAILURE": "Invalid code.",
    "SIGNING_ACTIVITY_SUCCESSFUL": "Sign in successful.",
    "SIGN OUT_ACTIVITY_SUCCESSFUL": "Sign-out successful.",
    "INVALID_TOKEN": "User provided an invalid token.",
    "PASSWORD_RESET": "Password Reset Successful.",
    "INVALID_FILE_TYPE": "File type not allowed.",
    "INVALID_FILE_EXTENSION": "File extension not allowed.",
    "INVALID_FILE_HEADER": "File header not allowed.",
    "FILE_TOO_LARGE": "File size not allowed. Allowed size is 16MB.",
    "FILE_UPLOAD_SUCCESSFUL": "File upload successful.",
    "FILE_UPLOAD_FAILURE": "File upload failed.",
    "INCORRECT_HEADER_MSG": "An error occured. There might be a possibility of an incorrect header used. Please check the header and try again."
}

MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'support@mystratify.com'
MAIL_PASSWORD = 'GdHRW5zWHTB2IIIsA85ixJhhmCaI4'