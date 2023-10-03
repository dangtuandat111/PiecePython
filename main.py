# This is a sample Python script.
import json

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

x = 0;
def format_log(log):
    results = log.split(' ')
    results = [s for s in results if s]

    global x
    x += 1

    temp = {
        "[STT]": x,
        results[4]: results[5],
        results[6]: results[7],
        results[8]: json.loads((' '.join(results[9:-3])) + ' }'),
    }

    return temp

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Define the desired title to filter by
    desired_title = '[ENGAGE_MOBILE-721]:'

    # Open and read the log file
    with open('C:/Users/dat.dangtuan/Desktop/Log/Folder/000000 (9)', 'r', encoding="utf8") as file:
        log_entries = file.readlines()

    # Initialize a list to store filtered log entries
    filtered_entries = []

    # Loop through each log entry
    for entry in log_entries:
        # Split the log entry into components (assuming space-separated)
        parts = entry.split()

        # Assuming 'title' is at a specific position (e.g., index 2)
        if len(parts) >= 4 and parts[3].__contains__(desired_title):
            # If the 'title' field matches the desired title, add it to the filtered list
            filtered_entries.append(format_log(entry))

    output_file_path = 'result.txt'

    # Write the filtered log entries to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(filtered_entries, output_file, indent=4)

