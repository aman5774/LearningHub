import math
def isprime(input_number):
    i_sqrt = int(math.sqrt(input_number))
    i = 2
    while(i < i_sqrt+1):
        if input_number%i == 0:
            return False
        i += 1
    if i == i_sqrt+1 :
        return True

if __name__ == '__main__':
    input_number = 2
    print(isprime(input_number))
