# DSP LAB FALL 2015
# Richard Shen
# Assignment 2

import random
import my_sort_methods


def main():
    random_list = [random.randint(0, 100) for c in range(10)]
    print "Original Random Array:        Before", random_list
    my_sort_methods.selectionSort(random_list)
    print "Using selection sort:         After " ,random_list

    sorted_list = my_sort_methods.quickSort(random_list)
    print "Using quicksort:              After " , sorted_list

if __name__ == '__main__':
  main()
