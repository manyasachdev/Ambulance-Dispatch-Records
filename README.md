# Ambulance-Dispatch-Records
Part of SaveLIFE Foundation's technical evaluation

This Python script analyzes and visualizes emergency call data from ambulance dispatch records. The dataset consists of two sheets: EventLog and ResponseTime.

Objective:

Develop a Python script to analyze and visualize emergency call data.

Data Description:

EventLog Sheet: Contains records of all calls received by the ambulance operator. Key columns include CALL_TIME, CALL_TYPE, CHIEF_COMPLAINT, and PRIORITY.

ResponseTime Sheet: Contains information on calls where an ambulance was dispatched, including Vehicle_Movement_Time, Vehicle_Atscene_Time, Response_Time, Handover_Time, and Handover_duration.

## Implementation Details and How to Run:

1. Clone this repository to your local machine. Ensure you have Python 3.7.4 installed.
2. Install the required dependencies using pip:

    ```
    pip install pandas matplotlib seaborn
    ```

4. Place your event log and response time datasets in CSV format in the same directory as the script.
5. Modify the `filepath_resp` and `filepath_event` variables in the script to point to your dataset files.
6. Run the script using the following command:

    ```
    python visualize_data.py
    ```

7. The visualizations will be displayed.

## File Structure

- `visualize_data.py`: Main Python script containing the implementation.
- `README.md`: Instructions on how to run the script and any dependencies required.
