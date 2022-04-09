import sys

# Function to perform booths algorithm
# Accepts as input a multiplier and multiplicand
# Returns the product of the two numbers
def booth(multiplier, multiplicand):
    n = len(multiplier)                 # n is the number of bits being used
    qn1 = '0'                           # qn+1 is set to 0
    ac = '0' * n                        # the ac starts as 0s
    counter = n                         # counter for how many times to loop through the alogrithm

    print("Initial\t\t", ac, multiplier, '0')

    while True:
        qn = multiplier[n-1]    # get the last bit of the multipler, q

        # If the last bit of the multiplier, q, and qn+1 are 10, subtract the multipler from the accumulator
        if (qn, qn1) == ('1', '0'):
            ac = bin(int(ac, 2) + int(twoscomp(multiplicand), 2))[2:].zfill(n)
            if len(ac) > n: ac = ac[len(ac)-n:]
            print("Subtract\t", ac, multiplier, qn1)

        # Else if the last bit of the multiplier, q, and qn+1 are 01, add the multiplier to the accumulator
        elif (qn, qn1) == ('0', '1'):
            ac = bin(int(ac, 2) + int(multiplicand, 2))[2:]
            if len(ac) > n: ac = ac[len(ac)-n:]
            print("Add\t\t", ac, multiplier, qn1)
        
        # Perform an arithmetic right shift on the contents of the accumulator, multiplier, and qn+1
        ac, multiplier, qn1 = ars(ac, multiplier, qn1)
        print("Shift\t\t", ac, multiplier, qn1)

        # Decrement the counter
        counter = counter - 1

        # If the counter reaches zero, break out of the loop
        if counter == 0:
            break
    
    # Return the contents of the accumulator and the multipler as a single string
    return (ac + multiplier)

# Function to perform the arithmetic right shift
# Accepts as input the accumulator (ac), the multiplier (mult), and qn+1 (qn1)
# Returns ac, mult, and qn1 post shift as a three tuple
def ars(ac, mult, qn1):
    combined = ac + mult + qn1
    combined = (combined[0] + bin(int(combined, 2) >> 1)[2:]).zfill(len(combined))
    return combined[:len(ac)], combined[len(ac):len(ac)+len(mult)], combined[len(ac)+len(mult):]

# Function to perform a binary two's compliment translation
# Accepts as single number as input
# Returns the two's compliment of that number
def twoscomp(num):
    num_len = len(num)
    num = list(num)
    for i in range(num_len):
        if num[i] == '1': num[i] = '0'
        else: num[i] = '1'
    return bin(int(''.join(num), 2) + 1)[2:].zfill(num_len)

if __name__ == "__main__":
    multiplicand = str(sys.argv[1])
    multiplier = str(sys.argv[2])

    product = booth(multiplier, multiplicand)

    # If the most significant print of the product is a 1, this indicates the answer is negative
    # Therefore, the product is set to the two's compliment translation of the product
    if product[0] == '1':
        product = twoscomp(product)
        print(f"Product = {product}, -{int(product, 2)}")

    else: print(f"Product = {product}, {int(product, 2)}")