class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, filePath=None):
     
        self.rows = 0
        self.cols = 0
        self.matrix = {}  # Dictionary of dictionaries: {row: {col: value}}
        
        if filePath is not None:
            self._load_from_file(filePath)
        elif numRows is not None and numCols is not None:
            self.rows = numRows
            self.cols = numCols
        else:
            raise ValueError("Must provide either dimensions or file path")
    
    def _load_from_file(self, filePath):
        """Load matrix data from file with custom parsing"""
        try:
            with open(filePath, 'r') as f:
                lines = [line.strip() for line in f if line.strip() != '']
                
                # Parse dimensions
                if not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                    raise ValueError("Invalid file format - missing dimensions")
                
                self.rows = int(lines[0][5:])
                self.cols = int(lines[1][5:])
                
                # Parse matrix entries
                for line in lines[2:]:
                    # Remove all whitespace
                    line = ''.join(line.split())
                    
                    
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError(f"Invalid entry format: {line}")
                    
                    
                    content = line[1:-1].split(',')
                    if len(content) != 3:
                        raise ValueError(f"Invalid entry format: {line}")
                    
                    # Parse values
                    try:
                        row = int(content[0])
                        col = int(content[1])
                        value = int(content[2])
                    except ValueError:
                        raise ValueError(f"Non-integer value in entry: {line}")
                    
                    # Validate indices
                    if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                        raise ValueError(f"Index out of bounds in entry: {line}")
                    
                    # Store non-zero values
                    if value != 0:
                        if row not in self.matrix:
                            self.matrix[row] = {}
                        self.matrix[row][col] = value
                        
        except IOError as e:
            raise IOError(f"Error reading file: {e}")
        except Exception as e:
            raise ValueError(f"Invalid file format: {e}")
    
    def getElement(self, currRow, currCol):
        """Get element at (currRow, currCol)"""
        if currRow < 0 or currRow >= self.rows or currCol < 0 or currCol >= self.cols:
            raise IndexError("Index out of bounds")
        
        return self.matrix.get(currRow, {}).get(currCol, 0)
    
    def setElement(self, currRow, currCol, value):
        """Set element at (currRow, currCol) to value"""
        if currRow < 0 or currRow >= self.rows or currCol < 0 or currCol >= self.cols:
            raise IndexError("Index out of bounds")
        
        if value == 0:
            
            if currRow in self.matrix and currCol in self.matrix[currRow]:
                del self.matrix[currRow][currCol]
                if not self.matrix[currRow]:  
                    del self.matrix[currRow]
        else:
            if currRow not in self.matrix:
                self.matrix[currRow] = {}
            self.matrix[currRow][currCol] = value
    
    def add(self, other):
        """Add another matrix to this matrix"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        
        result = SparseMatrix(self.rows, self.cols)
        
        # Copy all elements from self
        for row in self.matrix:
            for col in self.matrix[row]:
                result.setElement(row, col, self.getElement(row, col))
        
        # Add elements from other matrix
        for row in other.matrix:
            for col in other.matrix[row]:
                current = result.getElement(row, col)
                result.setElement(row, col, current + other.getElement(row, col))
        
        return result
    
    def subtract(self, other):
        """Subtract another matrix from this matrix"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")
        
        result = SparseMatrix(self.rows, self.cols)
        
        # Copy all elements from self
        for row in self.matrix:
            for col in self.matrix[row]:
                result.setElement(row, col, self.getElement(row, col))
        
        # Subtract elements from other matrix
        for row in other.matrix:
            for col in other.matrix[row]:
                current = result.getElement(row, col)
                result.setElement(row, col, current - other.getElement(row, col))
        
        return result
    
    def multiply(self, other):
        """Multiply this matrix with another matrix"""
        if self.cols != other.rows:
            raise ValueError("Number of columns in first matrix must match number of rows in second matrix")
        
        result = SparseMatrix(self.rows, other.cols)
        
        # Precompute transpose of other matrix for efficient column access
        other_transpose = {}
        for row in other.matrix:
            for col in other.matrix[row]:
                if col not in other_transpose:
                    other_transpose[col] = {}
                other_transpose[col][row] = other.matrix[row][col]
        
        # Perform multiplication
        for i in self.matrix:
            for k in other_transpose:
                dot_product = 0
                # Compute dot product of row i of self and column k of other
                for j in self.matrix[i]:
                    if j in other_transpose[k]:
                        dot_product += self.matrix[i][j] * other_transpose[k][j]
                if dot_product != 0:
                    result.setElement(i, k, dot_product)
        
        return result
    
    def save_to_file(self, filePath):
       
        with open(filePath, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            
            # Get all non-zero entries sorted by row and column
            entries = []
            for row in sorted(self.matrix.keys()):
                for col in sorted(self.matrix[row].keys()):
                    entries.append(f"({row},{col},{self.matrix[row][col]})\n")
            
            f.writelines(entries)

def main():
    print("Sparse Matrix Operations")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    
    try:
        choice = int(input("Enter operation (1-3): "))
        if choice not in [1, 2, 3]:
            raise ValueError("Invalid choice")
        
        file1 = input("Enter path to first matrix file: ")
        file2 = input("Enter path to second matrix file: ")
        output_file = input("Enter path for output file: ")
        
        # Load matrices
        matrix1 = SparseMatrix(filePath=file1)
        matrix2 = SparseMatrix(filePath=file2)
        
        # Perform operation
        if choice == 1:
            result = matrix1.add(matrix2)
        elif choice == 2:
            result = matrix1.subtract(matrix2)
        elif choice == 3:
            result = matrix1.multiply(matrix2)
        
        # Save the result
        result.save_to_file(output_file)
        print(f"Operation completed successfully. Result saved to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()