msg = "tomerbs1810@gmail.com"


def add_chars_to_msg(msg):
    data = b""
    if len(msg.encode()) < 320:
        data += msg.encode()
        for i in range(320 - len(msg.encode())):
            data += '|'.encode()

    return data


def remove_added_chars(msg):
    og_data = str(msg.decode())
    filtered_data = og_data.replace("|", "")
    return filtered_data


if __name__ == "__main__":
    msg = "tomerbs1810@gmail.com"
    ans_func1 = add_chars_to_msg(msg)
    print(ans_func1)

    ans_func2 = remove_added_chars(ans_func1)
    print(ans_func2)
