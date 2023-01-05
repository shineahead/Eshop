

code_str = string.ascii_letters + string.digits


def gen_code(len=4):
    return ''.join(random.sample(code_str, len))
