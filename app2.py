from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

def xml_to_dict(element):
    """
    Recursively converts an XML element and its children to a dictionary.
    """
    node_dict = {}
    if element.attrib:
        node_dict.update(element.attrib)
    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag not in node_dict:
            node_dict[child.tag] = child_dict
        else:
            if isinstance(node_dict[child.tag], list):
                node_dict[child.tag].append(child_dict)
            else:
                node_dict[child.tag] = [node_dict[child.tag], child_dict]
    if element.text and element.text.strip():
        node_dict['text'] = element.text.strip()
    return node_dict

@app.route('/get_library_data', methods=['POST'])
def get_library_data():
    if 'xml_file' in request.files:
        xml_file = request.files['xml_file']
        if xml_file.filename.endswith('.nml'):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Convert the entire XML structure to a dictionary
                nml_dict = xml_to_dict(root)
                
                # Return the dictionary as a JSON response
                return jsonify(nml_dict), 200
            except ET.ParseError as parse_error:
                return jsonify({'error': f"XML Parse Error: {str(parse_error)}"}), 500
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Only NML files are allowed.'}), 400
    else:
        return jsonify({'error': 'No file provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
