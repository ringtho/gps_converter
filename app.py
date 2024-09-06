# from flask import Flask, request, jsonify, send_file
# from pyproj import Proj
# import pandas as pd
# import io
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# def convert_utm_to_36N(coords, from_zone):
#     if from_zone == '35M':
#         utm_proj_from = Proj(proj='utm', zone=35, south=True, ellps='WGS84')
#     elif from_zone == '36M':
#         utm_proj_from = Proj(proj='utm', zone=36, south=True, ellps='WGS84')
#     elif from_zone == '35N':
#         utm_proj_from = Proj(proj='utm', zone=35, ellps='WGS84')
#     else:
#         raise ValueError("Invalid from_zone value. Use '35M' or '36M'.")

#     utm_proj_36N = Proj(proj='utm', zone=36, ellps='WGS84')
#     converted_coords = []

#     for easting_from, northing_from in coords:
#         lon, lat = utm_proj_from(easting_from, northing_from, inverse=True)
#         easting_36N, northing_36N = utm_proj_36N(lon, lat)
#         converted_coords.append((easting_36N, northing_36N))

#     return converted_coords

# def save_to_excel(original_coords, converted_coords):
#     data = {
#         'Easting_From': [coord[0] for coord in original_coords],
#         'Northing_From': [coord[1] for coord in original_coords],
#         'Easting_36N': [coord[0] for coord in converted_coords],
#         'Northing_36N': [coord[1] for coord in converted_coords]
#     }
#     df = pd.DataFrame(data)
#     output = io.BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False)
#     writer.close()
#     output.seek(0)
#     return output

# @app.route('/upload', methods=['POST'])
# @cross_origin()
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     from_zone = request.form.get('from_zone')
#     if from_zone not in ['35M', '36M', '35N']:
#         return jsonify({'error': 'Invalid from_zone value'}), 400

#     df = pd.read_excel(file)
#     coords = list(zip(df['Easting_From'], df['Northing_From']))
#     converted_coords = convert_utm_to_36N(coords, from_zone)
#     output = save_to_excel(coords, converted_coords)

#     return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='converted_coords.xlsx')

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, request, jsonify, send_file, send_from_directory
from pyproj import Proj
import pandas as pd
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

def convert_utm_to_36N(coords, from_zone):
    if from_zone == '35M':
        utm_proj_from = Proj(proj='utm', zone=35,south=True, ellps='WGS84')
    elif from_zone == '36M':
        utm_proj_from = Proj(proj='utm', zone=36, south=True, ellps='WGS84')
    elif from_zone == '35N':
        utm_proj_from = Proj(proj='utm', zone=35, ellps='WGS84')
    else:
        raise ValueError("Invalid from_zone value. Use '35M' or '36M'.")

    utm_proj_36N = Proj(proj='utm', zone=36, ellps='WGS84')
    converted_coords = []

    for easting_from, northing_from in coords:
        lon, lat = utm_proj_from(easting_from, northing_from, inverse=True)
        easting_36N, northing_36N = utm_proj_36N(lon, lat)
        converted_coords.append((easting_36N, northing_36N))

    return converted_coords

def save_to_excel(original_coords, converted_coords):
    data = {
        'Easting_From': [coord[0] for coord in original_coords],
        'Northing_From': [coord[1] for coord in original_coords],
        'Easting_36N': [coord[0] for coord in converted_coords],
        'Northing_36N': [coord[1] for coord in converted_coords]
    }
    df = pd.DataFrame(data)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    output.seek(0)
    return output

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    from_zone = request.form.get('from_zone')
    if from_zone not in ['35M', '36M', '35N']:
        return jsonify({'error': 'Invalid from_zone value'}), 400

    df = pd.read_excel(file)
    coords = list(zip(df['Easting_From'], df['Northing_From']))
    converted_coords = convert_utm_to_36N(coords, from_zone)
    output = save_to_excel(coords, converted_coords)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='converted_coords.xlsx')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)