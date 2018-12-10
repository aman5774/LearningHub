def linear_search(input_arr, search_element):
    for ielement in input_arr:
        if search_element == ielement:
            return True
    return False

if __name__ == '__main__':
    input_arr = map(int, raw_input("Input values separated by space:\n").strip().split())
    search_element = int(raw_input("Enter search element:"))
    print(linear_search(input_arr, search_element))
