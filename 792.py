import json

# File paths
input_file_path = "LOG/ERROR_59_Log.txt"
output_file_path = "LOG/ERROR_59_Log.txt"

try:
    # Read JSON data from the input file
    with open(input_file_path, "r") as input_file:
        json_data = json.load(input_file)

    # Format the JSON data for better readability (indent with 4 spaces)
    formatted_json = json.dumps(json_data, indent=4)

    data = [5865328,6101865,5516755,5724382,6209238,5842254,5350170,5593119,5762501,5724450,5299154,5133821,2489785,2437598,5617964,6285814,6291547,6274824,6396685,6294046,6222233,6051081,6274859,6396800,6396721,6274811,6396705,6396747,4279483,6396821,858130,5723980,5577019,4844276,6318025,5614425,2884867,4505952,1837141,5762445,3493954,5617280,5392088,2343859,126219,65614,5813963,65603,65610,2585225,6165461,65602,168961,3041085,3470514,1949426,1486160,4524499,2841428,6105306]

    print(len(data))

    print(len(json_data['paidPublication']['works']))

    # Write the formatted JSON data to the output file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(formatted_json)


    print(f"Formatted JSON data written to {output_file_path}")

except FileNotFoundError:
    print(f"Input file '{input_file_path}' not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"Error: {e}")