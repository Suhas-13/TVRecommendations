<template>
  

  <div class="py-6">
  <div class="flex flex-wrap max-width-show max-height-show bg-white shadow-lg rounded-lg overflow-hidden">
    <div v-if="image_url !== 'no-image'" class="width-bg-image bg-cover" v-bind:style="{ backgroundImage: 'url(' + image_url + ')' }"> </div> 
    <div v-if="image_url == 'no-image'" class="width-bg-image bg-contain" v-bind:style="{ backgroundImage: 'url(' + no_image_found + ')' }"> </div>
    <div class="width-text p-4">
      <h1 class="text-gray-900 font-bold text-2xl" v-html="outputHtml"></h1>
      <p class="mt-2 text-gray-600 text-sm">{{shortenedSummary}}</p>
      <div class="mt-5">
        <button v-if="display_only == false && added == false" @click = "addShow()" style = "justify-content: center;" class="px-3 py-2 bg-gray-800 text-white text-xs font-bold uppercase rounded">Add Show</button>
        <button v-if="display_only == false && added == true" @click = "removeShow()" style = "justify-content: center;" class="px-3 py-2 bg-gray-800 text-white text-xs font-bold uppercase rounded">Remove Show</button>
      </div>
    </div>
  </div>
</div>
  
</template>
<style>
  .max-width-show {
    min-width: 34rem;
    max-width:34rem;
  }
  .max-height-show {
    min-height: 12rem;
    max-height: 17rem;
  }
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
import {Show} from '../Show.js';
export default {
  name: 'Show',
  props: {
    name: String,
    highlightedName:  String,
    id: Number,
    display_only: Boolean,
    overview: String,
    publishedDate: String,
    image_url: String,
    added: Boolean
  },
  data: function(){
      return {max_summary_length: 26, no_image_found: require("../assets/no-image-icon.png")};
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
  },
  methods: {
    addShow() {
      this.$parent.addShow(new Show(this.name, this.id, this.overview, this.publishedDate, this.image_url, this.highlightedName));
    },
    removeShow() {
      this.$parent.removeShow(new Show(this.name, this.id, this.overview, this.publishedDate, this.image_url, this.highlightedName));
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>