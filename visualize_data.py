#Import Dependencies
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data Preparation
def load_data(filepath_event, filepath_resp):
    """
    Ojective of function: 
        1. Load the datasets from the given file paths
        2. Handle any missing values appropriately
        3. Convert the CALL_TIME column to datetime format.

    Parameters:
        filepath_event (type str): The file path for the event log data.
        filepath_resp (type str): The file path for the response time data.

    We can take several appraoches to dealing with missing values:
    Approach 1: Remove rows with missing values
        This approach works well if the number of rows affected is relatively small. 
        However, in the given dataset, since the number of rows with missing values
        in over 50%, we stand to lose a lot of valuable data. 
    Approach 2: Imputation
        This refers to the practice of replacing null values with common estimations.
        These include mean, median, mode or even a constant value. This doesn't seem
        to be necessary for our use case at this moment.

    """
    event_log_df = pd.read_csv(filepath_event)
    response_time_df = pd.read_csv(filepath_resp)

    event_log_df['CALL_TIME'] = pd.to_datetime(event_log_df['CALL_TIME'])
    response_time_df['CALL_TIME'] = pd.to_datetime(response_time_df['CALL_TIME'])

    #Merging the datasets for easier handling
    merged_df = pd.merge(event_log_df, response_time_df, on='EVENT_ID', how='outer', suffixes=('_event', '_response'))
    
    return event_log_df, response_time_df, merged_df

# Data Analysis 
def analyze_data(merged_df):
    """
    Ojective of function: 
        1. Calculate the total number of calls for each CALL_TYPE
        2. Determine the most common CHIEF_COMPLAINT
        3. Analyze the distribution of PRIORITY levels.

    Parameters:
    merged_df
    """
    call_type_counts = merged_df['CALL_TYPE_event'].value_counts() + merged_df['CALL_TYPE_response'].value_counts()
    common_complaint = merged_df['CHIEF_COMPLAINT'].mode()[0]
    priority_distribution = merged_df['PRIORITY'].value_counts()
    
    return call_type_counts, common_complaint, priority_distribution
    #print(priority_distribution)
    #print("Most common complaint = ", common_complaint)
    #print(call_type_counts)

# Detailed Analysis on PRIORITY levels
def analyze_priority_distribution(merged_df):

    """
    Objective of the function:
    Add additional visualisations related to PRIORITY for a more granular, in-depth analysis

    Parameters:
    merged_df
    """

    # Group by CALL_TYPE and calculate priority distribution
    priority_by_call_type = merged_df.groupby('CALL_TYPE_event')['PRIORITY'].value_counts(normalize=True).unstack().fillna(0) + merged_df.groupby('CALL_TYPE_response')['PRIORITY'].value_counts(normalize=True).unstack().fillna(0)
    # Group by CHIEF_COMPLAINT and calculate priority distribution
    priority_by_complaint = merged_df.groupby('CHIEF_COMPLAINT')['PRIORITY'].value_counts(normalize=True).unstack().fillna(0)

    # PRIORITY Heatmaps
    # Plotting the heatmap for priority distribution by CALL_TYPE
    sns.heatmap(priority_by_call_type, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title('Priority Distribution by CALL_TYPE')
    plt.xlabel('PRIORITY')
    plt.ylabel('CALL_TYPE')
    plt.tight_layout()
    plt.show()

    # Plotting the heatmap for priority distribution by CHIEF_COMPLAINT
    sns.heatmap(priority_by_complaint, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title('Priority Distribution by CHIEF_COMPLAINT')
    plt.xlabel('PRIORITY')
    plt.ylabel('CHIEF_COMPLAINT')
    plt.tight_layout()
    plt.show()

# Data Visualisation
def visualize_data(call_type_counts, priority_distribution, merged_df):
    """
    Objective of the function:
    1. Create a bar chart showing the total number of calls for each CALL_TYPE
    2. Create a pie chart showing the distribution of different PRIORITY levels.
    3. Create a line chart showing the number of calls over time (by month).

    Parameters: call_type_counts, priority_distribution, merged_df
    """

    # Bar chart for total number of calls for each CALL_TYPE
    plt.figure(figsize=(10, 6))
    sns.barplot(x=call_type_counts.index, y=call_type_counts.values)
    plt.title('Total Number of Calls for Each CALL_TYPE')
    plt.xlabel('CALL_TYPE')
    plt.ylabel('Number of Calls')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Pie chart for distribution of PRIORITY levels
    plt.figure(figsize=(8, 8))
    priority_distribution.plot.pie(autopct='%1.1f%%')
    plt.title('Distribution of PRIORITY Levels')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

    # Line chart for number of calls over time
    merged_df['CALL_TIME_event_MONTH'], merged_df['CALL_TIME_response_MONTH'] = merged_df['CALL_TIME_event'].dt.to_period('M'), merged_df['CALL_TIME_response'].dt.to_period('M') 
    calls_over_time = merged_df['CALL_TIME_event_MONTH'].value_counts().sort_index() + merged_df['CALL_TIME_response_MONTH'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    calls_over_time.plot()
    plt.title('Number of Calls Over Time (by Month)')
    plt.xlabel('Month')
    plt.ylabel('Number of Calls')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main Function
def main():
    # Set File paths
    filepath_resp = r'C:\Users\manya\Downloads\savelife_responsetime.csv'
    filepath_event = r'C:\Users\manya\Downloads\savelife_eventlog.csv'

    event_log_df, response_time_df, merged_df = load_data(filepath_event, filepath_resp)
    call_type_counts, common_complaint, priority_distribution = analyze_data(merged_df)
    
    print(f'Total number of calls for each CALL_TYPE:\n{call_type_counts}\n')
    print(f'Most common CHIEF_COMPLAINT: {common_complaint}\n')
    print(f'Distribution of PRIORITY levels:\n{priority_distribution}\n')

    visualize_data(call_type_counts, priority_distribution, merged_df)
    analyze_priority_distribution(merged_df)

if __name__ == '__main__':
    main()