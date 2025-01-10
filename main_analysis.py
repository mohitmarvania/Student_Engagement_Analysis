import os
from datetime import datetime, date
from ultralytics import YOLO
import cv2
from pathlib import Path
import pandas as pd
import model_prediction

folder_to_analyze = "./screenshots"


# Function to create the folder structure
def create_folder_structre(time_noted):
    global folder_to_analyze

    # Check if the folder exists or not.
    analysed_folder = "./Analysed"
    if not os.path.exists(analysed_folder):
        os.makedirs(analysed_folder)

    # Create a folder with the current date inside the "Analysed" folder
    current_date = datetime.now().strftime("%d-%m-%Y")
    analysed_data_folder = os.path.join(analysed_folder, f"Analyses_{current_date}_{time_noted}")
    if not os.path.exists(analysed_data_folder):
        os.makedirs(analysed_data_folder)

    return analysed_data_folder


# Helper function to check if folder is empty or not.
def is_folder_empty(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return False

    # List contents of the folder
    folder_contents = os.listdir(folder_path)

    if folder_contents:
        return True


# Helper function to print the result
# def print_result(result):
#     global word_before
#     results_lower = result.lower()
#     # Iterate through the list of words
#     for emotion in emotions:
#         # Convert the word to lowercase
#         emotion_lower = emotion.lower()
#         # Check if the word is present in the results
#         if emotion_lower in results_lower:
#             # Find the index of the word in the results
#             index = results_lower.find(word_lower)
#
#             # Extract the two characters before the word
#             if index >= 2:
#                 word_before = results[index - 2:index]
#             else:
#                 word_before = results[:index]
#
#     return word_before, emotion


def run_the_analysis(output_folder_path, time_started, faculty_name_selected, ss_saved_folder):
    engaged_count, frustrated_count, sleepy_count, bored_count, confused_count, yawning_count = model_prediction.model_predict(
        output_folder_path, ss_saved_folder)

    print("Engaged : ", engaged_count)
    print("Frustrated : ", frustrated_count)
    print("Sleepy : ", sleepy_count)
    print("Bored : ", bored_count)
    print("Confused : ", confused_count)
    print("Yawning : ", yawning_count)
    print("FACULTY NAME : ", faculty_name_selected)

    engagement_level_avg = (engaged_count + confused_count) // 2
    disengagement_level_avg = (frustrated_count + sleepy_count + bored_count + yawning_count) // 4

    if engagement_level_avg != 0 and disengagement_level_avg != 0:
        final_eng_level = (engagement_level_avg / (engagement_level_avg + disengagement_level_avg)) * 100
        final_diseng_level = (disengagement_level_avg / (engagement_level_avg + disengagement_level_avg)) * 100
    else:
        final_eng_level = 0.00
        final_diseng_level = 0.00

    final_eng_level = round(final_eng_level, 2)
    final_diseng_level = round(final_diseng_level, 2)

    # Get the current date and time
    current_date = date.today().strftime("%Y-%m-%d")

    # Create a Dataframe with the data
    analysed_data = pd.DataFrame({
        'Time': [time_started],
        'Faculty': [faculty_name_selected],
        'Engagement Level (%)': [final_eng_level],
        'Disengagement Level (%)': [final_diseng_level],
        'Engaged': [engaged_count],
        'Frustrated': [frustrated_count],
        'Sleepy': [sleepy_count],
        'Bored': [bored_count],
        'Confused': [confused_count],
        'Yawning': [yawning_count],
    })

    # Set the file name for the Excel file
    excel_file_name = f"Analysed_data_{current_date}.xlsx"

    # Set the path for the Excel file
    downloads_folder = Path.home() / "Downloads"
    excel_file_path = downloads_folder / excel_file_name

    # Check if the file already exists
    if os.path.isfile(excel_file_path):
        # If the file exists, append the data to the existing file
        existing_data = pd.read_excel(excel_file_path)
        updated_data = pd.concat([existing_data, analysed_data], ignore_index=True)
        updated_data.to_excel(excel_file_path, index=False)
    else:
        # If the file does not exists, create a new file with the data
        analysed_data.to_excel(excel_file_path, index=False)


def analysis_main(time_noted, faculty_name, ss_saved_folder):
    # Creating a folder
    output_folder = create_folder_structre(time_noted)

    # checking if the folder is empty or not.
    if not is_folder_empty(f"{ss_saved_folder}"):
        print("The folder do not contains screenshots..!!")
        return

    run_the_analysis(output_folder, time_noted, faculty_name, ss_saved_folder)
