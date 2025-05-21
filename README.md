# Sparse Matrix Implementation in Python

This project implements a sparse matrix data structure and operations as part of the "Data Structures and Algorithms for Engineers" Programming Assignment 2.

## Project Structure

```
dsa/
└── sparse_matrix/
    ├── src/               # Source code
    │   ├── sparse_matrix.py   # Main implementation
    │   ├── main.py            # Command-line interface
    │   └── test_sparse_matrix.py  # Unit tests
    └── sample_inputs/     # Sample matrix input files
        ├── matrix1.txt
        ├── matrix2.txt
        └── matrix3.txt
```

## Implementation Details

### SparseMatrix Class

The sparse matrix is implemented using a dictionary-based approach where only non-zero elements are stored in memory. Each non-zero element is mapped from its position (row, column) to its value:

```python
self.elements = {}  # Dictionary to store non-zero elements: (row, col) -> value
```

This implementation optimizes memory usage and operations for matrices that contain mostly zero elements.

### Key Features

1. **Memory Efficiency**: Only non-zero elements are stored in memory
2. **Input Handling**: Robust parsing of matrix files with proper error checking
3. **Matrix Operations**: Efficient implementations of:
   - Addition
   - Subtraction
   - Multiplication
4. **Exception Handling**: Proper error handling for invalid inputs and operations

### Matrix Operations

#### Addition and Subtraction
- Time Complexity: O(n + m) where n and m are the number of non-zero elements in each matrix
- Memory Complexity: O(n + m) in the worst case

#### Multiplication
- Time Complexity: O(n * m) where n is the number of non-zero elements in the first matrix and m is the number of non-zero elements in the second matrix that can be multiplied with elements in the first matrix
- Space Complexity: O(p) where p is the number of non-zero elements in the result matrix

## How to Run

### Requirements
- Python 3.6 or higher

### Running the Program

```bash
# Navigate to the source directory
cd dsa/sparse_matrix/src/

# Run the main program
python main.py
```

### Running Tests

```bash
# Navigate to the source directory
cd dsa/sparse_matrix/src/

# Run the tests
python test_sparse_matrix.py
```

## Usage Instructions

When you run the program, you'll be presented with a menu:

```
================== Sparse Matrix Operations ==================
1. Addition
2. Subtraction
3. Multiplication
4. Exit
Enter your choice (1-4):
```

For each operation, you'll need to provide:
1. Path to the first matrix file
2. Path to the second matrix file
3. Path for the output result file

### Input File Format

The program reads sparse matrices from files with the following format:

```
rows=4
cols=5
(0, 0, 10)
(0, 3, 12)
(1, 1, -3)
...
```

Where:
- First line specifies the number of rows
- Second line specifies the number of columns
- Each subsequent line specifies a non-zero element in the format `(row, column, value)`

## Error Handling

The program handles several error conditions:
- Invalid file format
- Missing files
- Matrix dimension mismatches for operations
- Invalid matrix indices
- Out-of-range operations

## Code Documentation

The code is thoroughly documented with:
- Class and method descriptions
- Parameter explanations
- Error handling notes
- Comprehensive unit tests

## Implementation Notes