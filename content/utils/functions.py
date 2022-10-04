def validation_create_data(data: dict) -> dict:
    keys = data.keys()
    result = {}

    if "title" not in keys:
        result["title"] = "missing key"
    elif type(data["title"]) != str:
        result["title"] = "must be a str"

    if "module" not in keys:
        result["module"] = "missing key"
    elif type(data["module"]) != str:
        result["module"] = "must be a str"

    if "description" not in keys:
        result["description"] = "missing key"
    elif type(data["description"]) != str:
        result["description"] = "must be a str"

    if "students" not in keys:
        result["students"] = "missing key"
    elif type(data["students"]) != int:
        result["students"] = "must be a int"

    if "is_active" not in keys:
        result["is_active"] = "missing key"
    elif type(data["is_active"]) != bool:
        result["is_active"] = "must be a bool"

    return result


def data_processing(data: dict) -> dict:
    keys = data.keys()
    result = {}

    if "title" in keys:
        result["title"] = data["title"]

    if "module" in keys:
        result["module"] = data["module"]

    if "description" in keys:
        result["description"] = data["description"]

    if "students" in keys:
        result["students"] = data["students"]

    if "is_active" in keys:
        result["is_active"] = data["is_active"]

    return result


def validation_update_data(data: dict) -> dict:
    keys = data.keys()
    result = {}

    if "title" in keys:
        if type(data["title"]) != str:
            result["title"] = "must be a str"

    if "module" in keys:
        if type(data["module"]) != str:
            result["module"] = "must be a str"

    if "description" in keys:
        if type(data["description"]) != str:
            result["description"] = "must be a str"

    if "students" in keys:
        if type(data["students"]) != int:
            result["students"] = "must be a int"

    if "is_active" in keys:
        if type(data["is_active"]) != bool:
            result["is_active"] = "must be a bool"

    return result
