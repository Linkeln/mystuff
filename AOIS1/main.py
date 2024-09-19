# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def swap_zeros_ones(string):
    swapped = ""
    for char in string:
        if char == '0':
            swapped += '1'
        elif char == '1':
            swapped += '0'
        else:
            swapped += char

    return swapped
def straight_to_decimal(binary):
    decimal = 0
    power = len(binary) - 1

    for bit in binary:
        if bit == '1':
            decimal += 2 ** power
        power -= 1

    return decimal
def decimal_to_binary(decimal):
    binary = ""

    if decimal == 0:
        binary = "0"

    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal // 2
    binary = (8 - len(binary)) * '0' + binary
    return binary


def decimal_to_binary_reversed(decimal):
    binary = ''
    neg = True
    if decimal >= 0:
        neg = False
    if decimal == 0:
        binary = '0'
    decimal = abs(decimal)
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal // 2
    binary = (8 - len(binary)) * '0' + binary
    if neg:
        binary = swap_zeros_ones(binary)
        binary = '1' + binary[1:]
    return binary
def reversed_to_additional(inverted):
    if inverted[0] == "0":
        return inverted
    else:
        newresult = ""
        for i in range(7, -1, -1):
            if inverted[i] == '0':
                newresult = inverted[:i] + "1" + newresult

                break
            else:
                newresult += "0"
        return newresult

def summ(num1, num2):
    reversed1 = (reversed_to_additional(decimal_to_binary_reversed(num1)))
    reversed2 = (reversed_to_additional(decimal_to_binary_reversed(num2)))
    carry = 0  # Перенос
    print(reversed1)
    print(reversed2)
    result = ""  # Результат сложения

    for i in range(7, -1, -1):
        bit_sum = int(reversed1[i]) + int(reversed2[i]) + carry

        if bit_sum >= 2:
            carry = 1
            bit_sum %= 2
        else:
            carry = 0

        result = str(bit_sum) + result

    return result

def summ_bin(num1, num2):
    carry = 0  # Перенос
    result = ""  # Результат сложения

    max_len = max(len(num1), len(num2))
    if len(num1) != len(num2):
        temp1 = num1[0]*abs(len(num1) - len(num2))
        if len(num1) < max_len:
            num1 = temp1 + num1
        else:
            num2 = temp1 + num2


    #for i in range(7, -1, -1): #сделать не воьмибитную границу а по максимальной длине
    for i in range(max_len - 1, -1, -1):
        bit_sum = int(num1[i]) + int(num2[i]) + carry

        if bit_sum >= 2:
            carry = 1
            bit_sum %= 2
        else:
            carry = 0

        result = str(bit_sum) + result

    return result

def subtract(num1, num2):
    num2 = -num2
    return summ(num1, num2)


def mult(num1, num2):
    binary1 = decimal_to_binary(num1)
    binary2 = decimal_to_binary(num2)
    loop = 0
    result = "00000000"
    temp = ""
    for i in range(7, -1, -1):
        if binary2[i] == "1":
            temp = binary1 + ("0" * loop)
        else:
            temp = (len(binary1) + loop) * "0"
        loop += 1
        temp = temp[:8]
        result = summ_bin(temp, result)


    return result

def binary_division(dividend, divisor):
    dividend = straight_to_decimal(dividend)
    divisor = straight_to_decimal(divisor)
    print(dividend, divisor)

    quotient = 0
    remainder = 0

    dividend_str = bin(dividend)[2:]
    print(dividend_str)
    for bit in dividend_str:
        remainder = (remainder << 1) | int(bit)
        print(bit)
        if remainder >= divisor:
            remainder -= divisor
            quotient = (quotient << 1) | 1
        else:
            quotient = (quotient << 1)

    quotient = straight_to_decimal(str(quotient))
    remainder = straight_to_decimal(str(remainder))

    return quotient, remainder

import struct

def ieee754_addition(f1, f2):
    # Pack floats into IEEE 754 binary format
    def float_to_bin(f):
        return struct.unpack('>I', struct.pack('>f', f))[0]

    # Unpack binary to float
    def bin_to_float(b):
        return struct.unpack('>f', struct.pack('>I', b))[0]

    # Convert floats to binary representation
    bin1 = float_to_bin(f1)
    bin2 = float_to_bin(f2)

    # Extract sign, exponent, and mantissa
    sign1 = (bin1 >> 31) & 0x01
    sign2 = (bin2 >> 31) & 0x01
    exp1 = (bin1 >> 23) & 0xFF
    exp2 = (bin2 >> 23) & 0xFF
    mant1 = bin1 & 0x7FFFFF
    mant2 = bin2 & 0x7FFFFF

    # Add implicit leading 1 to mantissas
    mant1 |= 0x800000
    mant2 |= 0x800000

    # Align exponents
    if exp1 > exp2:
        mant2 >>= (exp1 - exp2)
        exp = exp1
    else:
        mant1 >>= (exp2 - exp1)
        exp = exp2

    # Add mantissas
    if sign1 == sign2:
        mant = mant1 + mant2
        sign = sign1
    else:
        if mant1 > mant2:
            mant = mant1 - mant2
            sign = sign1
        else:
            mant = mant2 - mant1
            sign = sign2

    # Normalize the result
    if mant & 0x1000000:  # Check for overflow
        mant >>= 1
        exp += 1
    else:
        while mant < 0x800000 and exp > 0:
            mant <<= 1
            exp -= 1

    # Remove implicit leading 1
    mant &= 0x7FFFFF

    # Handle underflow
    if exp <= 0:
        exp = 0
        mant = 0

    # Pack the result back into binary
    result_bin = (sign << 31) | (exp << 23) | mant

    # Convert back to float
    return bin_to_float(result_bin)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
