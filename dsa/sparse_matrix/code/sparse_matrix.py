class SparseMatrix:
    """
    A class for efficient storage and operations on sparse matrices.
    This implementation uses a dictionary to store non-zero elements.
    """
    
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        """
        Initialize a SparseMatrix object either from a file or with specified dimensions.
        
        Args:
            matrix_file_path (str, optional): Path to the file containing matrix data.
            num_rows (int, optional): Number of rows in the matrix.
            num_cols (int, optional): Number of columns in the matrix.
        """
        # Dictionary to store non-zero elements as (row, col): value
        self.elements = {}
        
        # Matrix dimensions
        self.num_rows = num_rows
        self.num_cols = num_cols
        
        # If a file path is provided, load the matrix from the file
        if matrix_file_path:
            self._load_from_file(matrix_file_path)
    
    def _load_from_file(self, file_path):
        """
        Load a sparse matrix from a file.
        
        Args:
            file_path (str): Path to the file.
            
        Raises:
            ValueError: If the file format is incorrect.
        """
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                
                # Extract rows and columns
                rows_line = lines[0]
                cols_line = lines[1]
                
                if not rows_line.startswith("rows="):
                    raise ValueError("Input file has wrong format: 'rows=' prefix missing")
                if not cols_line.startswith("cols="):
                    raise ValueError("Input file has wrong format: 'cols=' prefix missing")
                
                try:
                    self.num_rows = int(rows_line.split('=')[1])
                    self.num_cols = int(cols_line.split('=')[1])
                except (IndexError, ValueError):
                    raise ValueError("Input file has wrong format: invalid row/column specification")
                
                # Process each element
                for i in range(2, len(lines)):
                    line = lines[i].strip()
                    
                    # Check for proper parentheses
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format: element not enclosed in parentheses")
                    
                    # Extract values between parentheses
                    values_str = line[1:-1].strip()
                    values = [val.strip() for val in values_str.split(',')]
                    
                    # Check if there are exactly 3 values
                    if len(values) != 3:
                        raise ValueError("Input file has wrong format: each element must have row, column, and value")
                    
                    try:
                        row = int(values[0])
                        col = int(values[1])
                        value = int(values[2])
                    except ValueError:
                        raise ValueError("Input file has wrong format: non-integer values found")
                    
                    # Set the element in the matrix
                    self.set_element(row, col, value)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            if isinstance(e, ValueError) and "Input file has wrong format" in str(e):
                raise
            raise ValueError(f"Input file has wrong format: {str(e)}")
    
    def get_element(self, row, col):
        """
        Get the value at the specified position.
        
        Args:
            row (int): Row index.
            col (int): Column index.
            
        Returns:
            int: The value at the position, 0 if not set.
        """
        return self.elements.get((row, col), 0)
    
    def set_element(self, row, col, value):
        """
        Set the value at the specified position.
        
        Args:
            row (int): Row index.
            col (int): Column index.
            value (int): Value to set.
        """
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise IndexError(f"Position ({row}, {col}) is out of bounds for matrix of size {self.num_rows}x{self.num_cols}")
        
        if value == 0:
            # If value is 0, remove the entry if it exists
            self.elements.pop((row, col), None)
        else:
            # Otherwise, add or update the entry
            self.elements[(row, col)] = value
    
    def add(self, other):
        """
        Add another sparse matrix to this one.
        
        Args:
            other (SparseMatrix): The matrix to add.
            
        Returns:
            SparseMatrix: The result of the addition.
            
        Raises:
            ValueError: If the matrices have different dimensions.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError(f"Cannot add matrices of different dimensions: {self.num_rows}x{self.num_cols} and {other.num_rows}x{other.num_cols}")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        # Add elements from the first matrix
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)
        
        # Add elements from the second matrix
        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value + value)
        
        return result
    
    def subtract(self, other):
        """
        Subtract another sparse matrix from this one.
        
        Args:
            other (SparseMatrix): The matrix to subtract.
            
        Returns:
            SparseMatrix: The result of the subtraction.
            
        Raises:
            ValueError: If the matrices have different dimensions.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError(f"Cannot subtract matrices of different dimensions: {self.num_rows}x{self.num_cols} and {other.num_rows}x{other.num_cols}")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        # Add elements from the first matrix
        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)
        
        # Subtract elements from the second matrix
        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value - value)
        
        return result
    
    def multiply(self, other):
        """
        Multiply this matrix by another sparse matrix.
        
        Args:
            other (SparseMatrix): The matrix to multiply with.
            
        Returns:
            SparseMatrix: The result of the multiplication.
            
        Raises:
            ValueError: If the number of columns in the first matrix doesn't match 
                       the number of rows in the second matrix.
        """
        if self.num_cols != other.num_rows:
            raise ValueError(f"Cannot multiply matrices with incompatible dimensions: {self.num_rows}x{self.num_cols} and {other.num_rows}x{other.num_cols}")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        
        # For each non-zero element in the first matrix
        for (row1, col1), value1 in self.elements.items():
            # Find all elements in the second matrix that share the same row as col1
            for (row2, col2), value2 in other.elements.items():
                if row2 == col1:
                    # Calculate the product and add it to the result
                    product = value1 * value2
                    current_value = result.get_element(row1, col2)
                    result.set_element(row1, col2, current_value + product)
        
        return result
    
    def save_to_file(self, file_path):
        """
        Save the sparse matrix to a file.
        
        Args:
            file_path (str): Path to the output file.
        """
        with open(file_path, 'w') as file:
            file.write(f"rows={self.num_rows}\n")
            file.write(f"cols={self.num_cols}\n")
            
            # Sort elements by row, then by column for consistent output
            sorted_elements = sorted(self.elements.items())
            
            for (row, col), value in sorted_elements:
                file.write(f"({row}, {col}, {value})\n")
    
    def __str__(self):
        """
        Return a string representation of the sparse matrix.
        
        Returns:
            str: String representation of the matrix.
        """
        result = [f"SparseMatrix({self.num_rows}x{self.num_cols})"]
        result.append(f"Non-zero elements: {len(self.elements)}")
        
        # Show up to 10 elements as a preview
        elements = list(self.elements.items())[:10]
        for (row, col), value in elements:
            result.append(f"({row}, {col}) = {value}")
        
        if len(self.elements) > 10:
            result.append(f"... and {len(self.elements) - 10} more elements")
            
        return "\n".join(result)