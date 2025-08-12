import csv
import re

# Path to the CSV file
csv_file_path = "/home/felix/F3/Namo/data/austria/better.csv"

# Initialize a set to collect unique invalid characters
invalid_characters = set()

# Open and read the CSV file
with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)

    # Iterate through rows in the CSV file
    for row in reader:
        if len(row) != 5:
            print(f"Row with unexpected number of columns: {row}")

        second_value = row[1]
        # Check if the second value contains anything other than A-Za-zÖÄÜöäü-
        if not re.fullmatch(r"[A-Za-zÖÄÜöäü-]+", second_value):
            # Collect invalid characters
            invalid_characters.update(re.findall(r"[^A-Za-zÖÄÜöäü-]", second_value))

            with open(
                "/home/felix/F3/Namo/data/austria/output.txt",
                mode="a",
                encoding="utf-8",
            ) as output_file:
                output_file.write(f"Line {reader.line_num}: {second_value}\n")
            print(f"Line {reader.line_num}: {second_value}")

# Write all collected invalid characters into the output file at the end
with open(
    "/home/felix/F3/Namo/data/austria/output.txt", mode="a", encoding="utf-8"
) as output_file:
    output_file.write(f"Invalid characters: {''.join(sorted(invalid_characters))}\n")
