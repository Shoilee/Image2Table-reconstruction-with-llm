import os
import json

# Paths
source_folder = 'true_label'        # Folder with original files (e.g., .html)
output_json_path = 'context.json'   # Output JSON file

# Output dictionary
output_data = {}

# Iterate over files in the source folder
for filename in os.listdir(source_folder):
    # Skip directories
    if not os.path.isfile(os.path.join(source_folder, filename)):
        continue

    # Extract basename (without extension)
    basename, _ = os.path.splitext(filename)
    
    with open(os.path.join(source_folder, filename), 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Add to output dictionary
    output_data[basename+".jpg"] = {
        "html": html_content,
        "type": "simple"
    }
   
# Write final JSON file
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=2)

print(f"DONE! JSON file written to: {output_json_path}")