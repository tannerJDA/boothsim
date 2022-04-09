import sys

def booth(multiplier, multiplicand):
    n = len(multiplier)        # n is the number of bits being used
    qn1 = '0'                           # qn+1 is set to 0
    ac = '0' * n                        # the ac starts as 0s
    counter = n

    print("Initial\t\t", ac, multiplier, '0')

    while True:
        qn = multiplier[n-1]    # get the last bit of the multipler

        if (qn, qn1) == ('1', '0'):
            ac = bin(int(ac, 2) + int(twoscomp(multiplicand), 2))[2:].zfill(n)
            if len(ac) > n: ac = ac[len(ac)-n:]
            print("Subtract\t", ac, multiplier, qn1)

        elif (qn, qn1) == ('0', '1'):
            ac = bin(int(ac, 2) + int(multiplicand, 2))[2:]
            if len(ac) > n: ac = ac[len(ac)-n:]
            print("Add\t\t", ac, multiplier, qn1)
        
        ac, multiplier, qn1 = ars(ac, multiplier, qn1)
        print("Shift\t\t", ac, multiplier, qn1)
        counter = counter - 1


        if counter == 0:
            break

    
    return (ac + multiplier)

# helper function to shift the ac, multiplier, and qn+1 bits together
def ars(ac, mult, qn1):
    combined = ac + mult + qn1
    combined = (combined[0] + bin(int(combined, 2) >> 1)[2:]).zfill(len(combined))
    return combined[:len(ac)], combined[len(ac):len(ac)+len(mult)], combined[len(ac)+len(mult):]

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

    if product[0] == '1':
        product = twoscomp(product)
        print(f"Product = {product}, -{int(product, 2)}")
    else: print(f"Product = {product}, {int(product, 2)}")