class Show {
    constructor(name, id, overview, date, image_url) {
        this.name = name;
        this.id = id;
        this.overview = overview;
        this.publishedDate = date;
        this.image_url = image_url;
        this.highlightedName = name;
    }
    highlightText(search_query) {
         this.highlightedName = this.name.replace(new RegExp(search_query, "ig"), function(matchedText){
              return ('<strong>' + matchedText + '</strong>');
        })
     }
    
}
export {Show};