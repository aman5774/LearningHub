def armstrong(input_number):
    temp = 0
    temp_input = input_number
    while(input_number > 0):
        num = input_number%10
        temp +=  num*num*num
        input_number //= 10
    if temp_input == temp:
        return True
    else:
        return False

if __name__ == "__main__":
    input_number = 153
    print(armstrong(input_number))
