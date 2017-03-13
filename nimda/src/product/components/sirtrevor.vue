<style src="ionicons/css/ionicons.css"></style>
<style src="sir-trevor/build/sir-trevor.css"></style>
<style lang="sass" src="../../styles/sirtrevor.scss"></style>

<template>
 <div>
  <textarea id="st" :value="product.sirtrevor | toString"></textarea>
</div>
</template>

<script>
import SirTrevor from '../../sirtrevor'
import store from '../store'


export default {
  computed: {
    product() {
      return store.state.product
    }
  },
  ready() {
    let editor = new SirTrevor.Editor({
      el: document.getElementById("st"),
      blockTypes: ["Product", "Markup", "Video", "Heading", "Text", "Image"]
    })
  }

}
</script>