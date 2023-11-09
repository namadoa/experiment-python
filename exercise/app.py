import re
from collections import Counter

def get_raghu_earnings(items_list, order_list):
    sizes_count = Counter(items_list)  # dictionary to keep track of shoe sizes
    earnings = 0  # initialize earnings
    
    # Process each customer order
    for size, price in order_list:
        if sizes_count[size] > 0:  # Check if the shoe size is available
            sizes_count[size] -= 1  # Reduce the count for the purchased size
            earnings += int(price)  # Add the price to the earnings
            
    return earnings  # Return the total earnings

def array_manipulation(n, queries):
    arr = [0] * (n + 1)  # Initialize array with an extra element to handle the range update efficiently
    
    # Apply each operation in the form of a range update
    for a, b, k in queries:
        arr[a - 1] += k  # Start of the range
        arr[b] -= k      # Just past the end of the range
    
    # Compute the prefix sum and find the max value
    max_value = -1
    current_sum = 0
    for i in range(n):
        current_sum += arr[i]
        max_value = max(max_value, current_sum)
    
    return max_value

def decode_matrix(matrix):
    # Combine characters from each column into a single string
    columns = zip(*matrix)
    decoded_string = ''.join(''.join(column) for column in columns)
    
    # Replace sequences of non-alphanumeric characters between alphanumerics with a single space
    readable_script = re.sub(r"(?<=[a-zA-Z0-9])[\s!@#$%&]+(?=[a-zA-Z0-9])", " ", decoded_string)
    
    return readable_script.strip()
