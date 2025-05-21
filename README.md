# Sparse Matrix Operations

A Python implementation for efficiently handling sparse matrices (matrices with mostly zero values). This implementation uses a memory-efficient dictionary-based storage approach.

## Features

- Memory-efficient sparse matrix representation
- Matrix operations: addition, subtraction, and multiplication
- File-based I/O for saving and loading matrices
- Command-line interface for matrix operations

## Usage

### Command Line Interface

Run the program and follow the interactive prompts:

```
python sparse_matrix.py
```

You'll be asked to:
1. Choose an operation (add, subtract, or multiply)
2. Provide paths to input matrix files
3. Specify an output file path

### File Format

Matrix files follow this format:
```
rows=3
cols=4
(0,0,5)
(1,2,7)
(2,1,3)
```

- First line: Number of rows
- Second line: Number of columns
- Subsequent lines: Non-zero entries as (row,col,value) tuples

### Programmatic Usage

```python
# Create a new matrix
matrix1 = SparseMatrix(3, 3)
matrix1.setElement(0, 0, 5)
matrix1.setElement(1, 2, 7)

# Load a matrix from file
matrix2 = SparseMatrix(filePath="matrix_file.txt")

# Perform operations
result = matrix1.add(matrix2)
# or
result = matrix1.subtract(matrix2)
# or
result = matrix1.multiply(matrix2)

# Save result
result.save_to_file("result_matrix.txt")
```

## Performance

The implementation is optimized for sparse matrices with mostly zero values. Operations only process non-zero elements, making it efficient for large sparse matrices.
