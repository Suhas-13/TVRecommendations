<template>
  <div class="about flex flex-col items-center">
    <div @click="modal=false" class ="absolute inset-0 z-0"> </div>
    <input class = "bg-gray-300 px-4 py-2 z-10"  @focus="modal=true" autocomplete = "off" type = "text" v-model="show">
    <div class ="z-10" v-if ="filteredShows && modal">
      <ul class="w-48 bg-gray-800 text-white">
        <li v-for="filteredShow in filteredShows" v-bind:key="filteredShow" class="py-2 border-b cursor-pointer" @click = "setShow(filteredShow)" v-html = "filteredShow"></li>
      </ul>
      </div>
  </div>
</template>
<script>
import {get_popular_shows, search} from '../api.js';
export default {
  data: function() {
    return {
      show: '',
      modal: false,
      maxResults: 5,
      filteredShows: [],
    }
  },
  mounted() {
    this.filterShows();
  },
  methods: {
    async filterShows() {
      if (this.show.length == 0) {
        const show_return = await get_popular_shows(this.maxResults);
        this.filteredShows.length = 0;
        for (let i=0; i<show_return.length; i++) {
          if (show_return[i]['name']) {
            this.filteredShows.push(show_return[i]['name']);
          }
        }
      }
      else {
        const show_return = await search(this.show, this.maxResults);
        this.filteredShows.length = 0;
        for (let i=0; i<show_return.length; i++) {
          var check = new RegExp(this.show, "ig");
          if (show_return[i]['name']) {
            this.filteredShows.push(show_return[i]['name'].replace(check, function(matchedText){
              return ('<strong>' + matchedText + '</strong>');
              }));
          }
        }

      }
    },
    setShow(show) {
      this.show = show;
      this.modal = false;
    }
  },
  watch: {
    show() {
      this.filterShows();
    }
  },

}

</script>
<style>
.highlightText {
        background: yellow;
    }
</style>