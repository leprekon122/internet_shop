def my_func(x: dict):
    res = []
    for key, value in x.items():
        res.append(float(value))
    result = min(res)

    for key_min, value_min in x.items():
        if (float(value_min) == result):
            return f" min_key = {key_min}, min_value = {value_min}"


if __name__ == "__main__":
    Numbers = {
        "number_1": "10.5",
        "number_2": 20,
        "number_3": 3.5,
        "number_4": "7",
        "number_5": 2,
        "number_6": "0.5",
        "number_7": "-2.5"
    }
    print(my_func(Numbers))
