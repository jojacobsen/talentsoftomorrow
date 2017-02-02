
def add_test_to_list(data, age, value, smaller_is_better):
    for d in data:
        if age == d[0]:
            # If test made on the same date just take the better one
            if smaller_is_better:
                if d[1] > value:
                    d[1] = value
                    return data
                else:
                    return data
            else:
                if d[1] < value:
                    d[1] = value
                    return data
                else:
                    return data

    data.append([age, value])
    return data


def round_test_list(data):
    # Round values
    for d in data:
        d[0] = round(d[0], 2)
        d[1] = round(d[1], 2)
    return data
