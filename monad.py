# %%
# DataFrame Monad

import pandas as pd

# DataFrame Monad class
class DataFrameMonad:
    def __init__(self, df):
        """Constructor for the DataFrame Monad."""
        self.df = df

    @staticmethod
    def unit(data):
        """Static method to construct a monad from initial data."""
        return DataFrameMonad(pd.DataFrame(data))

    def bind(self, func):
        """
        Monadic bind function:
        Takes a function 'func' that transforms the entire DataFrame.
        Returns a new DataFrameMonad with the transformed DataFrame.
        """
        transformed_df = func(self.df)  # Apply the function to the entire DataFrame
        return DataFrameMonad(transformed_df)

    def get(self):
        """Returns the current DataFrame."""
        return self.df


# Example function to handle duplicates
def handle_duplicates(df, column, resolve_func):
    """
    Detects duplicates in the specified 'column' and resolves them using 'resolve_func'.
    The resolve_func takes a group of duplicates and returns the value to keep.
    Removes all but one instance of the duplicate rows and updates the remaining row.
    """
    # def resolve_group(group):
    #     if len(group) > 1:
    #         # Apply the resolve function if there are duplicates
    #         chosen_value = resolve_func(group)
    #         return group.iloc[0].replace(group[column], chosen_value)
    #     return group.iloc[0]

    def resolve_group(group):
        if len(group) > 1:
            # Apply the resolve function if there are duplicates
            chosen_value = resolve_func(group)
            group.iloc[0, group.columns.get_loc(column)] = chosen_value
        return group.iloc[0]

    # Group by the column with potential duplicates
    deduplicated_df = (df.groupby(column, as_index=False)
                       .apply(lambda group: resolve_group(group))
                       .reset_index(drop=True))
    return deduplicated_df

# %%
# Example usage

# Step 1: Create initial data with duplicates
initial_data = {
    'A': [1, 2, 2, 3, 3, 3],
    'B': [10, 20, 25, 30, 35, 40],
    'C': [100, 200, 250, 300, 350, 400]
}

df_monad = DataFrameMonad.unit(initial_data)

print("Initial DataFrame before resolving duplicates:\n", df_monad.get())

# Define a resolve function (e.g., take the mean of column 'B' for duplicates)
def resolve_by_mean(group):
    return group['B'].mean()

# Step 2: Apply the handle_duplicates function using bind
result_monad = df_monad.bind(lambda df: handle_duplicates(df, 'A', resolve_by_mean))

# Step 3: Get the final transformed DataFrame
print("Final DataFrame after resolving duplicates:\n", result_monad.get())


# %%
# Define a List monad class

class ListMonad:
    def __init__(self, items):
        self.items = items

    @staticmethod
    def unit(items):
        return ListMonad(items)

    def bind(self, func):
        """Applies a function to each item in the list and returns a new ListMonad."""
        result = [func(item) for item in self.items]
        return ListMonad(result)

# Function to merge columns from one DataFrameMonad to another
def add_column_from_another_df(df, col_name, other_df):
    """Function to add a single column from another DataFrame."""
    df[col_name] = other_df[col_name]
    return df

# %%
# Example usage:

# Data in the original DataFrameMonad
initial_data = {
    'A': [1, 2, 3],
    'B': [10, 20, 30]
}

# Data in the second DataFrameMonad (that contains extra columns)
extra_data = {
    'C': [100, 200, 300],
    'D': [1000, 2000, 3000]
}

# Initialize two DataFrameMonads
df_monad = DataFrameMonad.unit(initial_data)
other_df_monad = DataFrameMonad.unit(extra_data)

print("Initial DataFrame:\n", df_monad.get())
print("Second DataFrame\n", other_df_monad.get())

# ListMonad containing the column names to add from the other DataFrameMonad
columns_to_add = ListMonad.unit(['C', 'D'])

# Iterate over the columns in the ListMonad and use bind to add them to the original DataFrame
result_monad = columns_to_add.bind(lambda col_name:
    df_monad.bind(lambda df: add_column_from_another_df(df, col_name, other_df_monad.get()))
)

# Get the updated DataFrame after adding the columns
print("Final DataFrame after adding columns from another DataFrame:\n", df_monad.get())

# %%
