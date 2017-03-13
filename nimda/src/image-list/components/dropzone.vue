<style src="dropzone/dist/dropzone.css"></style>
<style lang="sass" src="../../styles/dropzone.scss"></style>
<style>
#dzi {
  margin: 0px;
}
</style>

<template>
  <div id="dzi" class="dropzone"></div>
</template>


<script>
import Dropzone from 'dropzone'
import notie from '../../notie'

Dropzone.autoDiscover = false

export default {
  ready() {
    // setup dropzone
    let dz = new Dropzone("#dzi", {url: "dropzone/", uploadMultiple: true})
    dz.on('completemultiple', (files, res) => {
      setTimeout(() => { dz.removeAllFiles(true) }, 2000)
    })
    dz.on('successmultiple', (files, res) => {
      location.reload()
      notie.alert(4, 'Images successfully uploaded', 2)
    })
  }
}
</script>
