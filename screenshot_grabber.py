import time
import pyscreenshot as ImageGrabber
import schedule
from datetime import datetime
import os


def take_screenshot(time_noted):
    print(f"Taking Screenshot at {str(datetime.now())}")

    # Check if the screenshots folder exists, if not, create it
    folder_path = "./screenshots"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create a folder with the current date and time of starting inside the "screenshots" folder
    current_date = datetime.now().strftime("%d-%m-%Y")
    screenshot_folder = os.path.join(folder_path, f"screenshot_{current_date}_{time_noted}")
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    image_name = f"screenshot-{str(datetime.now())}"
    screenshot = ImageGrabber.grab()
    filepathloc = f"{screenshot_folder}/{image_name}.png"
    screenshot.save(filepathloc)
    print("Screenshot taken ... ")
    return screenshot_folder


def main(time_given):
    total_time = 20
    interval = 5

    folder_saved_screenshot = "./screenshots"

    if interval > total_time:
        raise ValueError("Interval should be smaller than total time!")

    # Calculate the number of times the screenshot should be taken
    num_screenshots = total_time // interval

    print(f"Num Screenshot : {num_screenshots}")

    for _ in range(num_screenshots):
        folder_saved_screenshot = take_screenshot(time_given)
        time.sleep(interval)

    return folder_saved_screenshot

    # schedule.every(5).seconds.do(take_screenshot)


# if __name__ == '__main__':
#     main("10:24:15 PM")
