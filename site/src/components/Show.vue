<template>
  <div class="show_item">
    <span v-html="outputHtml"></span>
    <br><br>
    <span> {{overview}} </span>
    <img v-bind:src="image_url">
  </div>
</template>

<script>

export default {
  name: 'Show',
  props: {
    name: String,
    highlightedName:  String,
    id: Number,
    overview: String,
    image_url: String
  },
  data: function(){
      return {max_summary_length: 10}
   },
  computed: {
    outputHtml: function() {
      return this.highlightedName;
    },
    shortenedSummary: function() {
      if (this.overview.split(" ").length > this.max_summary_length) {
        return this.overview.split(" ").slice(0,10).join(" ") + "...";
      }
      else {
        return this.overview.split(" ").slice(0,10).join(" ");
      }
      
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>