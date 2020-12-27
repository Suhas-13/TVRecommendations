<template>
  

  <div class="py-6">
  <div class="flex max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
    <div class="w-1/3 bg-cover" v-bind:style="{ backgroundImage: 'url(' + image_url + ')' }">
    </div> 
    <div class="w-2/3 p-4">
      <h1 class="text-gray-900 font-bold text-2xl" v-html="outputHtml"></h1>
      <p class="mt-2 text-gray-600 text-sm">{{shortenedSummary}}</p>
      <div class="flex item-center mt-2">
      
      </div>
      <div class="flex item-center justify-between mt-3">
        <h1 class="text-sm font-sans" style="color: #999">Published: {{publishedDate}}</h1>
        <button class="px-3 py-2 bg-gray-800 text-white text-xs font-bold uppercase rounded">Add to Card</button>
      </div>
    </div>
  </div>
</div>
  
</template>
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
      return {max_summary_length: 40}
   },
  computed: {
    outputHtml: function() {
      return this.highlightedName;
    },
    shortenedSummary: function() {
      if (this.overview.split(" ").length > this.max_summary_length) {
        return this.overview.split(" ").slice(0,this.max_summary_length).join(" ") + "...";
      }
      else {
        return this.overview.split(" ").slice(0,this.max_summary_length).join(" ");
      }
      
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>