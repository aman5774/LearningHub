def palindrome(input_number):
    rev_number = 0
    temp_input_num = input_number
    while(input_number > 0):
        rev_number = rev_number*10 + input_number%10
        input_number //= 10
    if temp_input_num == rev_number:
        return True
    else:
        return False

if __name__ == "__main__":
    input_number = 613
    print(palindrome(input_number))
