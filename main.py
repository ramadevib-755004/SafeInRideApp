from flask import Flask, render_template
import amadeus_service


app = Flask(__name__)

def change_keys_nested(json_list, key_map):
    for item in json_list:
        change_keys(item, key_map)
    return json_list

def change_keys(json_obj, key_map):
    for old_key, new_key in key_map.items():
        if old_key in json_obj:
            json_obj[new_key] = json_obj.pop(old_key)
            if isinstance(json_obj[new_key], dict):
                change_keys(json_obj[new_key], key_map)
            elif isinstance(json_obj[new_key], list):
                for sub_item in json_obj[new_key]:
                    if isinstance(sub_item, dict):
                        change_keys(sub_item, key_map)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/safeplace")
def safeplace():
    data = amadeus_service.safety_rated_locations()
    key_map = {'lgbtq' : 'LGBTQ',
           'medical': 'Medical',
           'overall': 'Overall',
   'physicalHarm': 'Physical Harm',
   'politicalFreedom': 'Political Freedom',
   'theft': 'Theft',
   'women': 'Women',
   'safetyScores':'safetyScores'}


    # Call the function to change the keys
    modified_list = change_keys_nested(data, key_map)

    

    return render_template('safeplace.html', safeplaces=modified_list)

@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
   app.run()