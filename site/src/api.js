import {Show} from './Show.js';
const PORT = 5128;
const BASE_URL = "https://recommend.suhas.net/api"
async function get_popular_shows(count) {
    const response = await fetch(BASE_URL + ":" + PORT + "/get-popular-shows?count=" + count, {method: 'GET', mode: 'cors'});
    const json_response = await response.json();
    if ("response" in json_response) {
        let output_list = [];
        for (let i=0; i<json_response['response'].length; i++) {
            let show = json_response['response'][i];
            output_list.push(new Show(show['name'], show['id'], show['overview'], show['published_date'], show['image_url']))
        }
        return output_list;
    }
    else {
        return [];
    }
}
async function search(query, count) {
    const response = await fetch(BASE_URL + ":" + PORT + "/search?query=" + query + "&count=" + count, {method: 'GET', mode: 'cors'});
    const json_response = await response.json();
    if ("response" in json_response) {
        let output_list = [];
        for (let i=0; i<json_response['response'].length; i++) {
            let show = json_response['response'][i];
            output_list.push(new Show(show['name'], show['id'], show['overview'], show['published_date'], show['image_url']))
        }
        return output_list;
    }
    else {
        return [];
    }
}
async function get_recommendations(show_id_list, count) {
    const data = {"show_id_list":show_id_list, "count":count};
    const response = await fetch(BASE_URL + ":" + PORT + "/generate_recommendation", {method: 'post', headers:{'Accept':'application/json','Content-Type':"application/json"}, body: JSON.stringify(data), mode: 'cors'});
    const json_response = await response.json();
    if ("response" in json_response) {
        let output_list = [];
        for (let i=0; i<json_response['response'].length; i++) {
            let show = json_response['response'][i];
            output_list.push(new Show(show['name'], show['id'], show['overview'], show['published_date'], show["image_url"]))
        }
        return output_list;
    }
    else {
        return [];
    }
}
export {get_popular_shows, search, get_recommendations}
