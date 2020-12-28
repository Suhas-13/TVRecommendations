<template>
  

  <div class="py-6">
  <div class="flex max-w-lg bg-white shadow-lg rounded-lg overflow-hidden">
    <div v-if="image_url !== 'no-image'" class="width-bg-image bg-cover" v-bind:style="{ backgroundImage: 'url(' + image_url + ')' }"> </div> 
    <div v-if="image_url == 'no-image'" class="width-bg-image bg-contain" v-bind:style="{ backgroundImage: 'url(' + no_image_found + ')' }"> </div>
   
    <div class="width-text p-4">
      <h1 class="text-gray-900 font-bold text-2xl" v-html="outputHtml"></h1>
      <p class="mt-2 text-gray-600 text-sm">{{shortenedSummary}}</p>
      <div class="justify-between mt-3">
        <button style = "justify-content: center;" class="px-3 py-2 bg-gray-800 text-white text-xs font-bold uppercase rounded">Mark as watched</button>
      </div>
    </div>
  </div>
</div>
  
</template>
<style>
  .width-bg-image {
    width: 28%;
  }
  .width-text {
    width: 72%;
  }
  .no-image {
    display: block;
    min-width: 300px;
    width: 300px;
    height: 450px;
    position: relative;
    top: 0;
    left: 0;
  }
</style>
Show number of episodes, ratings, description, name and image
<script>
export default {
  name: 'Show',
  props: {
    name: String,
    highlightedName:  String,
    id: Number,
    overview: String,
    publishedDate: String,
    image_url: String
  },
  data: function(){
      return {max_summary_length: 40, no_image_found: require("../assets/no-image-icon.png")}
   },
  computed: {
    outputHtml: function() {
      return this.highlightedName + "<br>(" + this.publishedYear + ")";
    },
    shortenedSummary: function() {
      if (this.overview.split(" ").length > this.max_summary_length) {
        return this.overview.split(" ").slice(0,this.max_summary_length).join(" ") + "...";
      }
      else {
        return this.overview.split(" ").slice(0,this.max_summary_length).join(" ");
      }
      
    },
    publishedYear: function() {
      return this.publishedDate.split("-")[0];
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>