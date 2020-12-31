import json
import time
show_save = json.load(open("show_save.json","r"))
keyword_save = json.load(open("keyword_save.json","r"))
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
    json.dump(show_save,open("show_save.json","w"))

def is_keyword_saved(keyword):
    return keyword in keyword_save
def get_stored_similar(keyword):
    if is_keyword_saved(keyword):
        return keyword_save[keyword]['keyword_list']
    else:
        return []
def save_keyword_list(keyword, keyword_list):
    keyword_save[keyword] = {"keyword_list":keyword_list,"added_utc":time.time()}
    json.dump(keyword_save,open("keyword_save.json","w"))