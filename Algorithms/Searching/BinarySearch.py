def binary_search(input_arr, search_element, low, high):
    mid = (low + high)//2
    if(low >= high):
        return False
    if(input_arr[mid] == search_element):
        return True
    elif(input_arr[mid] > search_element):
        return binary_search(input_arr, search_element, low, mid-1)
    elif(input_arr[mid] < search_element):
        return binary_search(input_arr, search_element, mid+1, high)

if __name__ == "__main__":
    input_arr = [1, 2, 3, 4, 5]
    search_element = 6
    print(binary_search(input_arr, search_element, 0, len(input_arr)))
