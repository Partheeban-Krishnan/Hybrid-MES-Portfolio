import joblib

# The file must be in the same directory as your script
filename = 'isolation_forest_model.pkl'

# Load the trained model
loaded_model = joblib.load(filename)

# You can now use 'loaded_model' to find anomalies in new data
# For example: loaded_model.predict(new_data)