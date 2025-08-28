import random

from string import digits


def generate_otp_code(l=4):
    otp_code = "".join([random.choice(digits) for _ in range(l)])
    return otp_code