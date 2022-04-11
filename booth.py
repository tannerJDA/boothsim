# =============================================================== #
# Purpose: 
# Authors: Samantha Baker, Tanner Armstrong                       #
# Date of Last Revision: 04.09.2022                               #
# =============================================================== #


import sys
import time

# Function to perform Booth's algorithm
# Accepts as input a multiplicand and multiplier
# Returns the product of the two numbers
def booth(multiplicand, multiplier):
    n = len(multiplicand)                 # n is the number of bits being used
    qn1 = '0'                           # qn+1 is set to 0
    ac = '0' * n                        # the ac starts as 0s
    counter = n                         # counter for how many times to loop through the alogrithm
    num_additions = 0
    num_subtractions = 0

    print("    AC   Q    Qn+1")
    print(f"    {ac} {multiplicand} 0   |  Initial value")

    start_time = time.time()
    while True:
        qn = multiplicand[n-1]    # get the last bit of the multipler, q

        # If the last bit of the multiplicand, q, and qn+1 are 10, subtract the multipler from the accumulator
        if (qn, qn1) == ('1', '0'):
            ac = bin(int(ac, 2) + int(twos_comp(multiplier), 2))[2:].zfill(n)
            if len(ac) > n: ac = ac[len(ac)-n:]
            print(f"    {ac} {multiplicand} {qn1}   |  Subtract multiplier")
            num_subtractions = num_subtractions + 1

        # Else if the last bit of the multiplicand, q, and qn+1 are 01, add the multiplicand to the accumulator
        elif (qn, qn1) == ('0', '1'):
            ac = bin(int(ac, 2) + int(multiplier, 2))[2:]
            if len(ac) > n: ac = ac[len(ac)-n:]
            print(f"    {ac} {multiplicand} {qn1}   |  Add multiplier")
            num_additions = num_additions + 1
        
        # Perform an arithmetic right shift on the contents of the accumulator, multiplicand, and qn+1
        ac, multiplicand, qn1 = ars(ac, multiplicand, qn1)
        print(f"    {ac} {multiplicand} {qn1}   |  Shift right")

        # Decrement the counter
        counter = counter - 1

        # If the counter reaches zero, break out of the loop
        if counter == 0:
            end_time = time.time()
            break
    
    print(f" Answer: \t{ac + multiplicand}\n\n Excec time: \t{end_time - start_time} seconds\n Iterations: \t{n}\n Additions: \t{num_additions}\n Subtractions: \t{num_subtractions}")
    # Return the contents of the accumulator and the multipler as a single string
    return (ac + multiplicand)

# Function to perform modified Booth's algorithm
# Accepts as input a multiplicand and multiplier
# Returns the product of the two numbers

def modified_booth(multiplicand, multiplier):
    twos = twos_comp(multiplicand)  # get the two's compliment of the multiplier
    padded = multiplier + "0"       # pad the muliplier to get recode results
    orglen = len(multiplicand)      # get the original length for filling
    maxlen = orglen * 2             # get max length for filling
    recode = []                     # empty list for recode results and dictionary for finding values
    recode_vals = {"001":1, "010":1, "011":2, "100":-2, "101":-1, "110":-1}
    result = 0                      # final result is currently 0

    # find the recode results for each set of 3 bits
    for b in range(0, len(padded), 2):
        if padded[b-2:b+1] in recode_vals: recode.insert(0, recode_vals.get(padded[b-2:b+1]))
        else: recode.insert(0, "0")

    # format printing
    temp = " "
    for c in range(len(recode)-1, -1, -1):
        temp += " " + str(recode[c])
    print(f"  Bit Recoding: {recode}\n    {multiplicand}\n  x{temp}\n--------------------------")

    # perform the multiplications using the recode results
    for c in range(len(recode)):
        # pad the end for each iteration
        if c > 0: 
            twos += "00"
            multiplicand += "00"
            orglen += 2
        
        # perform the multiplications
        if recode[c] == 1: recode[c] = bin(int(multiplicand, 2))[2:].zfill(orglen)
        if recode[c] == 2: recode[c] = bin((int(multiplicand + "0", 2)))[2:].zfill(orglen+1)
        if recode[c] == -2: recode[c] = bin((int(twos + "0", 2)))[2:].zfill(orglen+1)
        if recode[c] == -1: recode[c] = bin(int(twos, 2))[2:].zfill(orglen)

        # pad the beginning of each multiplication
        recode[c] = recode[c].rjust(maxlen, recode[c][0])

    # add all the multiplications together and format printing
    for r in range(len(recode)-1):
        print(f"    {recode[r]}")
        result += int(recode[r], 2)
    print(f"  + {recode[len(recode)-1]}\n--------------------------")
    result += int(recode[len(recode)-1], 2)

    # format printting
    if len(bin(result)[2:]) > maxlen:
        result = bin(result)[len(bin(result)[2:])-maxlen+2:]
        print(f"    {bin(int(result, 2))[2:].zfill(maxlen)}\n Answer: {bin(int(result, 2))[2:].zfill(maxlen)}")
        return bin(int(result, 2))[2:].zfill(maxlen)

    result = bin(result)
    end_time = time.time()
    print(f"    {bin(int(result, 2))[2:].zfill(maxlen)}\n Answer: {bin(int(result, 2))[2:].zfill(maxlen)}")
    return bin(int(result, 2))[2:].zfill(maxlen)


# Function to perform the arithmetic right shift
# Accepts as input the accumulator (ac), the multiplicand (mult), and qn+1 (qn1)
# Returns ac, mult, and qn1 post shift as a three tuple
def ars(ac, mult, qn1):
    combined = ac + mult + qn1
    combined = (combined[0] + bin(int(combined, 2) >> 1)[2:]).zfill(len(combined))
    return combined[:len(ac)], combined[len(ac):len(ac)+len(mult)], combined[len(ac)+len(mult):]


# Function to perform a binary two's compliment translation
# Accepts as single number as input
# Returns the two's compliment of that number
def twos_comp(num):
    num_len = len(num)
    num = list(num)
    for i in range(num_len):
        if num[i] == '1': num[i] = '0'
        else: num[i] = '1'
    return bin(int(''.join(num), 2) + 1)[2:].zfill(num_len)


if __name__ == "__main__":
    multiplier = str(sys.argv[1])
    multiplicand = str(sys.argv[2])

    print("\n === Booth's Algorithm ===")
    booth_product = booth(multiplicand, multiplier)

    # If the most significant print of the product is a 1, this indicates the answer is negative
    # Therefore, the product is set to the two's compliment translation of the product
    if booth_product[0] == '1':
        booth_product = twos_comp(booth_product)
        print(f"\n Booth's Product:\n  binary:\t{booth_product}\n  decimal:\t-{int(booth_product, 2)}")
    else: print(f"\n Booth's Product:\n  binary:\t{booth_product}\n  decimal:\t{int(booth_product, 2)}")

    print("\n\n === Modified Booth's Algorithm ===")
    modified_product = modified_booth(multiplicand, multiplier)

    # If the most significant print of the product is a 1, this indicates the answer is negative
    # Therefore, the product is set to the two's compliment translation of the product
    if modified_product[0] == '1':
        modified_product = twos_comp(modified_product)
        print(f"\n Modified Booth's Product:\n  binary:\t{modified_product}\n  decimal:\t-{int(modified_product, 2)}")
    else: print(f"\n Modiefied Booth's Product:\n  binary:\t{modified_product}\n  decimal:\t{int(modified_product, 2)}")
