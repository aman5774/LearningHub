def quicksort(arr, low, high):
    if(low < high):
        partition_index = partition(arr, low, high)
        quicksort(arr, low, partition_index-1)
        quicksort(arr, partition_index+1, high)

def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]
    for j in range(low, high):
        if(arr[j] <= pivot):
            i += 1
            arr[j], arr[i] = arr[i], arr[j]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1

if __name__ == '__main__':
    arr = [5,4,3,2,1]
    print("Input Array:\t" + ', '.join(list(map(str,arr))))
    low = 0
    high = len(arr) - 1
    quicksort(arr, low, high)
    print("Sorted Array:\t" + ', '.join(list(map(str,arr))))
