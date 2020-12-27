

<template>
  <div class="about flex flex-col items-center">
    <div @click="modal=false" class ="absolute inset-0 z-0"> </div>
    <input class = "w-4/12 bg-gray-300 px-4 py-5 z-10"  @focus="modal=true" autocomplete = "off" type = "text" v-model="show">
    <div class = "px-0 py-0 h-full flex flex-col items-center z-10" v-if ="show_list && modal">
      <ul class="w-full text-white">
        <li v-for="(filteredShow, index) in show_list" v-bind:key="index" class="h-full flex flex-col items-center py-1 cursor-pointer" @click = "setShow(show_list[index])">
          <Show v-bind:name="show_list[index].name" v-bind:publishedDate="show_list[index].publishedDate" v-bind:highlightedName="show_list[index].highlightedName" v-bind:id ="show_list[index].id" v-bind:overview="show_list[index].overview" v-bind:image_url="show_list[index].image_url"></Show>
        </li>
      </ul>
      </div>     

  </div>

</template>
<style>

</style>

<script>
import {get_popular_shows, search} from '../api.js';
import Show from '../components/Show.vue';
export default {
  name: "About",
  components: {
    Show
  },
  data: function() {
    return {
      show: '',
      show_id: '',
      modal: false,
      maxResults: 5,
      show_list: [],
    }
  },
  mounted() {
    this.filterShows();
  },
  methods: {
    async filterShows() {
      if (this.show.length == 0) {
        const show_return = await get_popular_shows(this.maxResults);
        this.show_list.length = 0;
        for (let i=0; i<show_return.length; i++) {
          if (show_return[i]['name']) {
            this.show_list.push(show_return[i]);
          }
        }
      }
      else {
        const show_return = await search(this.show, this.maxResults);
        this.show_list.length = 0;
        for (let i=0; i<show_return.length; i++) {
          if (show_return[i]['name']) {
            show_return[i].highlightText(this.show);
            this.show_list.push(show_return[i]);
          }
        }
      }
    },
    setShow(show) {
      this.show = show.name;
      this.show_id = show.id;
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