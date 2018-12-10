def substrings(input_str):
    out = list(input_str)
    token_length = 2
    i = 0
    n = len(input_str)
    while(token_length < n):
        i = 0
        while(i <= n-token_length):
            temp = ''
            j = 0
            while(j < token_length):
                temp += input_str[i+j]
                j += 1
            out.append(temp)
            i += 1
        token_length += 1
    out.append(input_str)
    return out

if __name__ == '__main__':
    input_str = 'ABCD'
    print(substrings(input_str))
