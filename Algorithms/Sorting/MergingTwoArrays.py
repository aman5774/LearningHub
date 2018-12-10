def MergeArrays(input_arr1, input_arr2):
    i = 0
    j = 0
    size_arr1 = len(input_arr1)
    size_arr2 = len(input_arr2)
    out_arr = []
    while(i < size_arr1 and j < size_arr2):
        if input_arr1[i] < input_arr2[j]:
            out_arr.append(input_arr1[i])
            i += 1
        elif input_arr1[i] > input_arr2[j]:
            out_arr.append(input_arr2[j])
            j += 1
        elif input_arr1[i] == input_arr2[j]:
            out_arr.append(input_arr1[i])
            out_arr.append(input_arr2[j])
            i += 1
            j += 1
    while i < size_arr1:
        out_arr.append(input_arr1[i])
        i += 1
    while j < size_arr2:
        out_arr.append(input_arr2[j])
        j += 1
    return out_arr

input_arr1 = [1,3,5,6]
input_arr2 = [2,3,4]

if __name__ == "__main__":
    print(MergeArrays(input_arr1, input_arr2))
