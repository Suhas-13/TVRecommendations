

<template>
  <div class="about flex flex-col items-center">
    <div @click="modal=false" class ="absolute inset-0 z-0"> </div>
    <input class = "bg-gray-300 px-4 py-2 z-10"  @focus="modal=true" autocomplete = "off" type = "text" v-model="show">
    <div class ="z-10" v-if ="show_list && modal">
      <ul class="w-48 bg-gray-800 text-white">
        <li v-for="(filteredShow, index) in show_list" v-bind:key="index" class="py-2 border-b cursor-pointer" @click = "setShow(filteredShow)">
          <Show v-bind:name="show_list[index].name" v-bind:highlightedName="show_list[index].highlightedName" v-bind:id ="show_list[index].id" v-bind:overview="show_list[index].overview" v-bind:image_url="show_list[index].image_url"></Show>
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