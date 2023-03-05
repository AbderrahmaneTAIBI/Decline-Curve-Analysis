# Decline Curve Analysis Web App
This is a web application for analyzing oil and gas production data using decline curve analysis. The app allows users to upload production data for a well, select a decline model (exponential, hyperbolic, harmonic, or stretched exponential), and visualize the production data and the fitted decline curve. The mean squared error (MSE) between the production data and the fitted decline curve is also displayed.

## Dependencies
* Dash
* Plotly
* NumPy
* Pandas
* SciPy
* dash-bootstrap-components

## Usage

To use the app, follow these steps:

1. Clone the repository to your local machine
2. Install the dependencies listed above
3. Run the 'DeclineCurveAnalysisDashboard.py' script in your terminal with the command python DeclineCurveAnalysisDashboard.py
4. Open your web browser and go to http://127.0.0.1:8050/ to access the web app

## How it works
The app loads synthetic decline curves from a CSV file and displays the production data for a selected well on a graph. The user can upload their own production data in CSV or Excel format. After selecting a well and a decline model, the app fits the model to the production data using the curve_fit function from the SciPy library. The fitted decline curve is then displayed on the graph, along with the mean squared error between the production data and the fitted curve. The user can switch between different wells, decline models, and uploaded datasets using dropdown menus.

## Files
DeclineCurveAnalysisDashboard.py: The main script that runs the app
synthetic_decline_curves.csv: A CSV file containing synthetic decline curves for multiple wells
synthetic_decline_curves2.csv: A CSV file containing synthetic decline curves for multiple wells in order to test theDrag and Drop section
README.md: This file

## Future improvements
* Troubleshoot the dropdown section and make it updated with the number of wells each time another dataset is introduced
* Add support for more decline models
* Improve the user interface
* Allow users to download the fitted decline curve as a CSV file

### Note
in order to use it the data has to be pre-processed in this format: 
<img width="656" alt="Screen Shot 2023-03-05 at 5 13 29 AM" src="https://user-images.githubusercontent.com/55601081/222941396-ab4285ff-cc9e-49bb-ba3a-7c67cff4d64b.png">

