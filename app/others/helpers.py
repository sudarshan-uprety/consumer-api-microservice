import json

from pydantic import ValidationError


def pydantic_error(errors_list):
    msg: dict = dict()
    for error in errors_list:
        # Build the nested error message
        new_msg: dict = dict()
        for key in reversed(error["loc"][1:]):
            if new_msg:
                new_msg = {key: new_msg}
            else:
                msg_key = " ".join(str(e).replace("_", " ").capitalize() for e in error["loc"])
                error_type = error.get("type", ".").split(".")[-1]
                msg_footer: str = ""
                if error_type == "bool":
                    msg_footer = "is not a valid value."
                elif error_type == "enum":
                    msg_footer = "is not a value that is permitted."
                elif error_type == "datetime":
                    msg_footer = "is not a value in datetime format."
                elif error_type == "min_length":
                    limit_value = error["ctx"]["limit_value"]
                    msg_footer = f"must have length greater than {limit_value}."
                elif error_type == "max_length":
                    limit_value = error["ctx"]["limit_value"]
                    msg_footer = f"must have length less than {limit_value}."
                elif error_type == "list":
                    msg_footer = "is not a permitted value."
                elif error_type == "not_gt":
                    limit_value = error["ctx"]["limit_value"]
                    msg_footer = f"must be greater than {limit_value}."
                elif error_type == "not_lt":
                    limit_value = error["ctx"]["limit_value"]
                    msg_footer = f"must be less than {limit_value}."
                elif error_type == "email":
                    msg_footer = "Value is not a valid email address."
                elif error_type == "regex":
                    msg_footer = (
                        "takes alphanumeric characters and symbols like ( ) / -."
                    )
                elif error_type == "integer":
                    msg_footer = "is not a valid number."
                elif error_type == "missing":
                    msg_footer = "is missing."
                else:
                    msg_footer = error["msg"]
                new_msg = {key: msg_key + " " + msg_footer}

        if error["loc"][0] in msg.keys():
            msg[error["loc"][0]][error["loc"][1]] = new_msg[error["loc"][1]]
        else:
            if new_msg:
                msg[error["loc"][0]] = new_msg
            else:
                msg[error["loc"][0]] = (
                    error["loc"][0].capitalize() + " " + error["msg"] + "."
                )
    return msg
