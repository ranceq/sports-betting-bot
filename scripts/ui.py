import streamlit as st
import pandas as pd
import os

# Set the title of the dashboard.
st.title("Daily Betting Predictions Dashboard")
st.markdown("Below are the bot’s predictions for today, including confidence values (scale 1–10).")

# Determine the path to your CSV file with daily results.
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "data", "daily_results.csv")

# Read the CSV file into a DataFrame.
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("The daily_results.csv file was not found. Please ensure the file exists in the data folder.")
    st.stop()

# Display basic statistics.
st.subheader("Summary Statistics")
st.write(df.describe())

# Add a filter for Sport.
st.subheader("Filter by Sport")
sports = df["Sport"].unique().tolist()
selected_sport = st.selectbox("Select a sport:", options=["All"] + sports)

# Add a slider to filter by minimum confidence.
min_confidence = st.slider("Minimum Confidence", min_value=1.00, max_value=10.00, value=5.00, step=0.01)

# Apply filtering.
if selected_sport != "All":
    filtered_df = df[(df["Sport"] == selected_sport) & (df["Confidence"] >= min_confidence)]
else:
    filtered_df = df[df["Confidence"] >= min_confidence]

# Display the filtered DataFrame.
st.subheader("Daily Predictions")
st.dataframe(filtered_df)

# Optionally, display the entire dataset.
if st.checkbox("Show all predictions"):
    st.subheader("All Daily Predictions")
    st.dataframe(df)

# Add some charts or visualizations (optional).
st.subheader("Confidence Distribution")
st.bar_chart(filtered_df["Confidence"].value_counts().sort_index())
