import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Function to import validation data
def import_val_data():
    val_data = pd.read_csv("merged.csv")
    val_data['TP.FP'] = val_data['TP.FP'].astype(str)  # Ensure TP.FP is string type
    val_data['Accuracy'] = val_data['TP.FP'].apply(lambda x: 1 if x == "TRUE" else 0)  # Create Accuracy column
    return val_data

# Function to analyze species using logistic regression
def analyze_species(data, accuracy_threshold):
    data['TP.FP'] = data['TP.FP'].astype(str)  # Ensure TP.FP is string type
    data['Accuracy'] = data['TP.FP'].apply(lambda x: 1 if x == "TRUE" else 0)  # Create Accuracy column
    
    # Split data by species
    species_list = data.groupby('Species')
    
    results = {}
    
    # Loop through each species
    for species, species_data in species_list:
        # Fit logistic regression model
        try:
            glm_model = sm.GLM(species_data['Accuracy'], sm.add_constant(species_data['Combined Confidence']), family=sm.families.Binomial()).fit()
            
            # Predict probabilities
            predicted = glm_model.predict(sm.add_constant(species_data['Combined Confidence']))
            
            # Find confidence where accuracy is at least the threshold
            confidence_value = species_data.loc[predicted >= accuracy_threshold, 'Combined Confidence'].iloc[0]
            
            results[species] = {'model': glm_model, 'confidence': confidence_value}
        
        except Exception as e:
            print(f"Error fitting model for {species}: {str(e)}")
            results[species] = {'model': None, 'confidence': 0.1}  # Default confidence value if model fitting fails
    
    return results

# Function to convert results to a DataFrame
def results_to_dataframe(results):
    df = pd.DataFrame([(species, result['confidence']) for species, result in results.items()],
                      columns=['Species', 'Confidence'])
    return df

# Function to make validation plot
def make_validation_plot(val_data):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=val_data, x='Combined Confidence', y='Accuracy', hue='Species', palette='Set1')
    plt.title('Validation Plot for Accuracy vs Combined Confidence')
    plt.xlabel('Combined Confidence')
    plt.ylabel('Accuracy')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('validation_plot.png')
    plt.show()

# Main function to perform analysis
def make_validation_df():
    val_data = import_val_data()
    results = analyze_species(val_data, accuracy_threshold=0.9)
    results_df = results_to_dataframe(results)
    print(results_df)
    results_df.to_csv('validation_thresholds.csv', index=False)
    make_validation_plot(val_data)

# Run the main function
if __name__ == "__main__":
    make_validation_df()
