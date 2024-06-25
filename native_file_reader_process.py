def determine_type(value):
    """
    This function attempts to determine the type of the given value.
    It returns the value converted to its detected type and the type itself.
    """
    if value.isdigit():
        return int(value), type(int(value))
    try:
        float_value = float(value.replace(',', '.'))
        return float_value, type(float_value)
    except ValueError:
        return value, type(value)

def native_csv_matrix_from_file_reader_process(file_path, original_delimiter=';', new_delimiter=';', original_decimal='.', new_decimal=',', print_mode=True, type_mode=False):
    # Read the file
    with open(file_path, 'r') as file:
        csv_data_contents = file.read()

        # Replace original delimiter with new delimiter and original decimal with new decimal
        modified_csv_data_contents = csv_data_contents.replace(original_delimiter, new_delimiter).replace(original_decimal, new_decimal)

        # Print the original and modified content if print_mode is True
        if print_mode:
            print("Original Data:\n", csv_data_contents)
            print("Modified Data:\n", modified_csv_data_contents)

        # Print the type of the modified content if type_mode is True
        if type_mode:
            print("Type of modified data:", type(modified_csv_data_contents))

    # Split the modified data into rows and then into columns to create a matrix
    csv_data_matrix = [row.split(new_delimiter) for row in modified_csv_data_contents.strip().split('\n')]

    return csv_data_matrix

def csv_data_submatrix(csv_data_matrix, start_row, end_row, start_col, end_col):
    # Extract the submatrix
    csv_data_submatrix = [row[start_col:end_col+1] for row in csv_data_matrix[start_row:end_row+1]]
    return csv_data_submatrix

def csv_data_matrix_cell_value(csv_data_matrix, i, j):
    """
    This function will return a tuple containing the value at the specified row and column index in the matrix,
    and its detected type.
    """
    try:
        if i >= 1 and j >= 1:
            value = csv_data_matrix[i-1][j-1]
            return determine_type(value)
    except IndexError:
        return None, None

def csv_data_matrix_row_vector(csv_data_matrix, i):
    """
    This function will return a list containing the values of the specified row index in the matrix,
    with each value converted to its detected type.
    """
    try:
        row_vector = csv_data_matrix[i-1]
        typed_row_vector = [determine_type(value) for value in row_vector]
        return typed_row_vector
    except IndexError:
        return None

def csv_data_matrix_column_vector(csv_data_matrix, j):
    """
    This function will return a list containing the values of the specified column index in the matrix,
    with each value converted to its detected type.
    """
    try:
        column_vector = [row[j-1] for row in csv_data_matrix]
        typed_column_vector = [determine_type(value) for value in column_vector]
        return typed_column_vector
    except IndexError:
        return None

def csv_data_matrix_type(csv_data_matrix):
    """
    Parses the entire CSV data matrix and returns a new matrix with tuples containing the value and its detected type.
    """
    parsed_matrix = []
    
    for i in range(1, len(csv_data_matrix)+1):
        parsed_row = []
        for j in range(1, len(csv_data_matrix[i-1])+1):
            parsed_row.append(csv_data_matrix_cell_value(csv_data_matrix, i, j))
        parsed_matrix.append(parsed_row)
    
    return parsed_matrix

def export_to_csv(parsed_matrix, filename, separator =";"):
    """
    Exports the parsed matrix to a CSV file with ';' as a separator.
    """
    with open(filename, mode='w', newline='') as file:
        for row in parsed_matrix:
            line = separator.join([f"{value}:{dtype}" for value, dtype in row])
            file.write(line + "\n")

# Example usage
file_path ='file.csv'
result = native_csv_matrix_from_file_reader_process(file_path)
print(result)

# Specify the submatrix range (start_row, end_row, start_col, end_col)
start_row = 1
end_row = 5
start_col = 1
end_col = 4

submatrix = csv_data_submatrix(result, start_row, end_row, start_col, end_col)
print("Extracted Submatrix:")
for row in submatrix:
    print(row)

# Specify the position (i, j)
i = 1
j = 1

value, value_type = csv_data_matrix_cell_value(result, i, j)
print(f"Value at position ({i}, {j}): {value}")
print(f"Type of the value: {value_type}")

# Specify the row index
row_index = 1

row_vector = csv_data_matrix_row_vector(result, row_index)
print(f"Row vector at index {row_index}:")
for value, value_type in row_vector:
    print(f"Value: {value}, Type: {value_type}")

parsed_matrix = csv_data_matrix_type(result)
for row in parsed_matrix:
    print(row)

export_to_csv(parsed_matrix, 'output.csv')
