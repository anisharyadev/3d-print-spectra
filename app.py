
import os
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to slice the file using CuraEngine
def slice_file(file_path):
    command = f'curaengine slice -v -l {file_path} -o output.gcode'
    subprocess.run(command, shell=True)

    # Placeholder values for print time and filament usage
    print_time = 120  # Example print time in minutes
    filament_used = 25.4  # Example filament used in grams

    return print_time, filament_used

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and (file.filename.endswith('.stl') or file.filename.endswith('.obj')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Process the file with CuraEngine
        print_time, filament_used = slice_file(file_path)

        # Price calculation
        material_cost_per_gram = 1699 / 1000  # Example: ₹1699 per kg of filament
        total_cost = (filament_used * material_cost_per_gram) + (print_time * 18.42)

        # Return the slicing result (price, print time, filament usage)
        return jsonify({
            'print_time': print_time,
            'filament_used': filament_used,
            'total_cost': total_cost,
            'estimated_price_with_margin': total_cost * 1.25  # 25% profit margin
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
