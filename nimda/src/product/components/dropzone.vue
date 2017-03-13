<style src="dropzone/dist/dropzone.css"></style>
<style lang="sass" src="../../styles/dropzone.scss"></style>
<style>
#dzp {
  margin-top: 60px;
}
</style>

<template>
  <div id="dzp" class="dropzone"></div>
</template>


<script>
import Dropzone from 'dropzone'
import store from '../store'
const { loadDetailImages, loadStoreImages } = store.actions

Dropzone.autoDiscover = false

export default {
  ready() {
    // setup dropzone
    let dz = new Dropzone("#dzp", {url: "dropzone/", uploadMultiple: true})
    dz.on('completemultiple', (files, res) => {
      setTimeout(() => { dz.removeAllFiles(true) }, 2000);
    })
    dz.on('successmultiple', (files, res) => {
      loadDetailImages()
      loadStoreImages()
    })
  }
}
</script>