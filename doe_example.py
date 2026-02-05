import pandas as pd
import itertools

# Define levels for each factor (e.g., 3 levels for each excipient)
levels_A = [0, 1, 2]  # e.g., low, medium, high for Excipient A
levels_B = [0, 1, 2]  # e.g., low, medium, high for Excipient B

# Generate full factorial design
factorial_design = list(itertools.product(levels_A, levels_B))
df = pd.DataFrame(factorial_design, columns=['Excipient_A', 'Excipient_B'])
print(df)
