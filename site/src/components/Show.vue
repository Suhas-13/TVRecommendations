<template>
  <div class="show_item">
    <span v-if="highlightedName !== null" v-html="highlightedName"></span>
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
      return {}
   },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>