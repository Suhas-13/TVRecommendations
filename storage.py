import json
import time
show_save = json.load(open("show_save.json","r"))
def is_show_id_saved(show_id):
    return show_id in show_save
def get_show_object(show_id):
    if is_show_id_saved(show_id):
        return show_save[show_id]
    else:
        return {}
def save_show_object(data):
    show_save[data['id']] = data
    show_save[data['id']]['added_utc'] = time.time()
    json.dump(show_save,open("show_save.json","w+"))
