# %%
# DataFrame Monad class

import pandas as pd

class DataFrameMonad:
    def __init__(self, df):
        """Constructor for the DataFrame Monad."""
        self.df = df

    @staticmethod
    def unit(data):
        """Static method to construct a monad from initial data."""
        return DataFrameMonad(pd.DataFrame(data))

    def bind(self, func, axis=0):
        """
        Monadic bind function:
        Takes a function 'func' and applies it to either rows or columns of the DataFrame.
        axis = 0: applies to rows (default)
        axis = 1: applies to columns
        Returns a new DataFrameMonad with the transformed DataFrame.
        """
        transformed_df = self.df.apply(func, axis=axis)
        return DataFrameMonad(transformed_df)

    def add_row(self, row_data):
        """Adds a new row to the DataFrame. Returns a new DataFrameMonad."""
        new_row_df = pd.DataFrame([row_data], columns=self.df.columns)
        new_df = pd.concat([self.df, new_row_df], ignore_index=True)
        return DataFrameMonad(new_df)

    def add_column(self, col_name, col_data):
        """Adds a new column to the DataFrame. Returns a new DataFrameMonad."""
        self.df[col_name] = col_data
        return DataFrameMonad(self.df)

    def get(self):
        """Returns the current DataFrame."""
        return self.df


# %%
# Example usage:

# Step 1: Create an initial monad with some data
initial_data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}

df_monad = DataFrameMonad.unit(initial_data)

# Step 2: Define a transformation function for rows
def transform_row(row):
    return row * 2  # Multiply all elements in a row by 2

# Apply transformation to rows using bind
transformed_monad = df_monad.bind(transform_row, axis=1)
print("Transformed DataFrame (Rows multiplied by 2):\n", transformed_monad.get())

# Step 3: Add a new row
new_row = {'A': 7, 'B': 8}
monad_with_new_row = transformed_monad.add_row(new_row)
print("\nDataFrame after adding a new row:\n", monad_with_new_row.get())

# Step 4: Add a new column
new_column_data = [10, 20, 30, 40]  # Note: must match the number of rows
monad_with_new_column = monad_with_new_row.add_column('C', new_column_data)
print("\nDataFrame after adding a new column:\n", monad_with_new_column.get())

# %%
