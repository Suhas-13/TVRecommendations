import {Show} from './Show.js';
async function get_popular_shows(count) {
    const response = await fetch("http://192.168.86.36:5000/get-popular-shows?count=" + count, {method: 'GET', mode: 'cors'});
    const json_response = await response.json();
    if ("response" in json_response) {
        let output_list = [];
        for (let i=0; i<json_response['response'].length; i++) {
            let show = json_response['response'][i];
            output_list.push(new Show(show['name'], show['id'], show['overview'], show['image_url']))
        }
        return output_list;
    }
    else {
        return [];
    }
}
async function search(query, count) {
    const response = await fetch("http://192.168.86.36:5000/search?query=" + query + "&count=" + count, {method: 'GET', mode: 'cors'});
    const json_response = await response.json();
    if ("response" in json_response) {
        let output_list = [];
        for (let i=0; i<json_response['response'].length; i++) {
            let show = json_response['response'][i];
            output_list.push(new Show(show['name'], show['id'], show['overview'], show['image_url']))
        }
        return output_list;
    }
    else {
        return [];
    }
}
export {get_popular_shows, search}