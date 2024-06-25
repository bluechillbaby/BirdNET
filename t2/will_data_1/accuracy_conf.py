import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Step 1: Read the CSV file into a pandas DataFrame
file_path = 'BirdNet_validation.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Step 2: Extract the necessary columns
df = df[['Species', 'Confidence ', 'TP.FP']]
df.columns = ['Species', 'Confidence', 'TP_FP']

# Step 3: Calculate the accuracy values
df['Accuracy'] = df['TP_FP'].apply(lambda x: 1 if x == 'T' else 0)

# Step 4: Plot accuracy versus confidence scores for each species
species_list = df['Species'].unique()
num_species = len(species_list)

# Define the grid size
num_rows = 5
num_cols = 2
fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(10, 14))

# Flatten the axes array for easy iteration
axes = axes.flatten()

for i, species in enumerate(species_list):
    species_df = df[df['Species'] == species]
    
    # Scatter plot
    sns.scatterplot(data=species_df, x='Confidence', y='Accuracy', ax=axes[i], label=species)
    
    # Step 5: Add a regression line
    X = species_df['Confidence'].values.reshape(-1, 1)
    y = species_df['Accuracy'].values
    
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)
    
    axes[i].plot(species_df['Confidence'], y_pred, label=f"{species} Regression Line", color='red')
    
    # Customize the subplot
    axes[i].set_xlabel('Confidence Score')
    axes[i].set_ylabel('Accuracy')
    axes[i].grid(True)
    axes[i].set_ylim(-0.1, 1.1)

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust layout
plt.tight_layout()
plt.show()
