# DSP LAB FALL 2015
# Richard Shen
# Assignment 2

def selectionSort(array):
   for fillslot in range(len(array)-1,0,-1):
       positionOfMax=0
       for location in range(1,fillslot+1):
           if array[location]>array[positionOfMax]:
               positionOfMax = location

       temp = array[fillslot]
       array[fillslot] = array[positionOfMax]
       array[positionOfMax] = temp

def quickSort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        return quickSort(less)+equal+quickSort(greater)
    else:
        return array
