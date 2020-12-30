

<template>
  <div class="about flex flex-col items-center">
    <h1>Add shows to the list</h1>
    <br><br>
    <div v-if="recommendation_generated==false" @click="modal=false" class ="absolute inset-0 z-0"> </div>
    <input placeholder="Search shows" class = "w-4/12 bg-gray-300 px-4 py-5 z-10"  @focus="modal=true; recommendation_generated=false;" autocomplete = "off" type = "text" v-model="show">
    <div class = "px-0 py-0 h-full flex flex-col items-center z-10" v-if ="show_list && modal && recommendation_generated==false">
      <ul class="w-full text-white">
        <li v-for="(filteredShow, index) in show_list" v-bind:key="index" class="h-full flex flex-col items-center py-1 cursor-pointer">
          <ShowComponent v-bind:name="show_list[index].name" v-bind:added = "final_id_list.includes(show_list[index].id)" v-bind:publishedDate="show_list[index].publishedDate" v-bind:highlightedName="show_list[index].highlightedName" v-bind:id ="show_list[index].id" v-bind:overview="show_list[index].overview" v-bind:image_url="show_list[index].image_url"></ShowComponent>
        </li>
      </ul>
    </div>  
    <div class = "px-0 py-0 h-full flex flex-col items-center z-10" v-if ="modal==false && final_list.length != 0 && recommendation_generated==false"><br><br><br><br><br><br><br><br><br>Added Show's
      <ul class="w-full text-white">
        <li v-for="(filteredShow2, index2) in final_list" v-bind:key="index2" class="h-full flex flex-col items-center py-1 cursor-pointer">
          <ShowComponent v-bind:name="final_list[index2].name" v-bind:added = "final_id_list.includes(final_list[index2].id)" v-bind:publishedDate="final_list[index2].publishedDate" v-bind:highlightedName="final_list[index2].highlightedName" v-bind:id ="final_list[index2].id" v-bind:overview="final_list[index2].overview" v-bind:image_url="final_list[index2].image_url"></ShowComponent>
        </li>
      </ul>
      <br><br>
      <button @click="generateRecommendation()" style = "justify-content: center;" class="px-3 py-2 bg-gray-800 text-white text-xs font-bold uppercase rounded">Generate Recommendations</button>
  </div>
    <div class = "px-0 py-0 h-full flex flex-col items-center z-10" v-if ="modal == false && recommendation_generated==true">
      <br><br>
      <h1> Recommendation(s): </h1>
      <br>
        <ul class="w-full text-white">
          <li v-for="(filteredShow3, index3) in output_list" v-bind:key="index3" class="h-full flex flex-col items-center py-1 cursor-pointer">
            <ShowComponent v-bind:name="output_list[index3].name" v-bind:display_only="true" v-bind:added = "false" v-bind:publishedDate="output_list[index3].publishedDate" v-bind:highlightedName="output_list[index3].highlightedName" v-bind:id ="output_list[index3].id" v-bind:overview="output_list[index3].overview" v-bind:image_url="output_list[index3].image_url"></ShowComponent>
          </li>
        </ul>
      </div>
  </div>
  

</template>
<style>

</style>

<script>
import {get_popular_shows, search, get_recommendations} from '../api.js';
import ShowComponent from '../components/Show.vue';
export default {
  name: "About",
  components: {
    ShowComponent
  },
  data: function() {
    return {
      show: '',
      modal: false,
      maxResults: 3,
      show_list: [],
      final_list: [],
      final_id_list: [],
      output_list: [],
      recommendation_generated: false
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
            console.log(show_return[i]);

          }
        }
      }
    },
    addShow(show) {
      this.final_list.push(show);
      this.final_id_list.push(show.id);
    },
    removeShow(show) {
      for (let i=0; i<this.final_list.length; i++) {
        if (show.id === this.final_list[i].id) {
          this.final_list.splice(i,1);
          this.final_id_list.splice(i,1);
          break;
        }
      }
    },
    async generateRecommendation() {
      this.output_list = await get_recommendations(this.final_id_list, 1);
      
      this.recommendation_generated = true;

    }
  },
  watch: {
    show() {
      this.filterShows();
    }
  },

}

</script>