async function get_popular_shows(count) {
    const response = await fetch("http://192.168.86.36:5000/get-popular-shows?count=" + count, {method: 'GET'});
    const json_response = await response.json();
    if ("response" in json_response) {
        return json_response['response']
    }
    else {
        return [];
    }
}
async function search(query, count) {
    const response = await fetch("http://192.168.86.36:5000/search?query=" + query + "&count=" + count, {method: 'GET'});
    const json_response = await response.json();
    if ("response" in json_response) {
        return json_response['response']
    }
    else {
        return [];
    }
}
export {get_popular_shows, search}