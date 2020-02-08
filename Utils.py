from dateutil.parser import parse
from TextSummarization.Constants import Type


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


# print(is_date("Monday at 12:01am"))
# print(is_date("xyz_not_a_date"))
# test_date_and_time = "sdasdas asd asdasd Monday at 12:01am"
# print(is_date(test_date_and_time))  # Fails

def getKeyLimitFromType(type: int):
    return{Type.DEFAULT: 10,
           Type.TERM_FREQUENCY: 7,
           Type.TERM_UNIQUENESS: 22,
           Type.INVERSE_DOCUMENT_FREQUENCY: 15
    }[type]


def getDictionaryAsString(inputDictionary: dict, type=Type.DEFAULT):
    key_count = 0
    keys_visited = 0
    result = ""
    term_limit = getKeyLimitFromType(type)
    for i in inputDictionary:
        keys_visited += 1
        # print(f'{i}: {inputDictionary[i]}', end="")
        result += i + ": " + str(inputDictionary[i])
        if keys_visited < len(inputDictionary):
            # print(", ", end="", sep="")
            result += ", "
        key_count += 1
        if key_count == term_limit:
            # print()
            result += "\n"
            key_count = 0
    result += "\n"

    return result


def convertListToString(input_list) -> str:
    """
    :param input_list:
    :return string:
    """
    temp_list = input_list
    final_list = []
    for i in temp_list:
        if i not in final_list:
            final_list.append(i)

    output = "".join(final_list)
    return output

