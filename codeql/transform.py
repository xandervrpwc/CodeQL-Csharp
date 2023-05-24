import sys
import json
import concurrent.futures
import os

def process_json_file(json_file_path, unique_entries, json_file_type):
    try:
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        # Validate JSON structure
        if "#select" not in json_data or "tuples" not in json_data["#select"]:
            raise ValueError(f"Invalid JSON structure in file: {json_file_path}")

        # Transform the data into the desired format
        for entry_tuple in json_data["#select"]["tuples"]:
            filename, functionname = entry_tuple
            entry = {"input": functionname, "type": json_file_type, "sourcefile": filename}

            # Convert the dictionary to a tuple
            entry_tuple = (entry["input"], entry["type"], entry["sourcefile"])

            # Check if the entry already exists in the set
            if entry_tuple not in unique_entries:
                # Add the entry to the set and transformed data list
                unique_entries.add(entry_tuple)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {json_file_path}")
    except Exception as e:
        print(f"An error occurred while processing file: {json_file_path}")
        print(str(e))


def main(json_file_paths):
    # Initialize an empty set to store unique entries
    unique_entries = set()

    # Process each JSON file concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the processing of each JSON file to the executor
        futures = []
        for json_file_path in json_file_paths:
            json_file_type = os.path.splitext(json_file_path.split('/')[-1])[0]
            future = executor.submit(process_json_file, json_file_path, unique_entries, json_file_type)
            futures.append(future)

        # Wait for all the submitted tasks to complete
        concurrent.futures.wait(futures)

    # Convert the set of tuples back to dictionaries
    transformed_data = [{"input": entry[0], "type": entry[1], "sourcefile": entry[2]} for entry in unique_entries]

    # Create the output dictionary
    output_data = {"results": transformed_data}

    # Write the merged data to a new JSON file
    output_json_path = sys.argv[1]
    
    with open(output_json_path, 'w') as output_json_file:
        json.dump(output_data, output_json_file)

    print("Data transformation completed successfully!")


if __name__ == "__main__":
    # Get the JSON file paths from the command-line arguments
    json_file_paths = sys.argv[2:]

    if len(json_file_paths) < 1:
        print("Please provide at least one JSON file path.")
        sys.exit(1)

    main(json_file_paths)
