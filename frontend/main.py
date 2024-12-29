import pandas as pd
import streamlit as st
from utils.snowflake import connect_to_snowflake


# Function to query Snowflake and get server metrics
def get_server_metrics():
    conn = connect_to_snowflake()
    cursor = conn.cursor()

    # Execute the query to fetch the server metrics data
    cursor.execute("SELECT * FROM SERVER_METRICS")
    results = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(results, columns=columns)

    # Close the connection
    conn.close()

    return df


# Main Streamlit function
def main():
    # Set page configuration for a better layout
    st.set_page_config(page_title="Server Metrics Dashboard", layout="wide")

    # Header for the page
    st.title("Server Metrics Dashboard")

    # Display the server metrics data
    st.subheader("Latest Server Metrics")

    # Fetch and display the server metrics from Snowflake
    df = get_server_metrics()
    st.write("Here are the most recent server metrics:")
    st.dataframe(df)

    # Add a nice separator line
    st.markdown("---")

    # Prompt input form
    with st.form(key="prompt_form", clear_on_submit=True):
        st.markdown("### Enter your prompt:")
        prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Display the prompt the user entered
            st.write(f"Prompt submitted: {prompt}")
            st.success("Prompt submitted successfully!")


# Run the app
if __name__ == "__main__":
    main()
