<style lang="sass">
.import-container {
  display: none;
}
.sorter-container {
  width: 100%;
  margin: 2px 0;
  position: relative;
  display: flex;
  justify-content: space-between;
}
.sorter-container.labels {
  margin-top: 0;
  display: block;
}
.sorter-container .icon {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -12px;
  margin-top: -12px;
  background: #fff;
  /*border: 1px solid #EAEAEA;*/
  width: 24px;
  height: 24px;
  color: #ccc;
  line-height: 1.7;
  text-align: center;
}
.imagesorter-target,
.imagesorter-store {
  position: relative;
  /*float: left;*/
  width: 49.5%;
  width: calc(50% - 6px);
  border: 1px solid #d2d6de;
  min-height: 166px;
  padding: 0 0 6px 6px;
  //overflow: hidden;
}
.imagesorter-target {
  /*margin-left: 1%;*/
  /*float: right;*/
}
.toggleImageSize {
  display: block;
  float: right;
  margin: 10px auto;
  -webkit-appearance: none;
  background-color: #eee;
  border: 1px solid #d2d6de;
  /*padding: 6px 11px;*/
  width: 35px;
  height: 35px;
  font-size: 16px;
}
.toggleImageSize:focus {
  outline: none;
}
.toggleImageSize .fa-search-minus, #toggleImageSize.state-active .fa-search-plus {
  display: none;
}
.toggleImageSize.state-active {
  background-color: #333;
  border-color: #000;
  color: #fff;
}
.toggleImageSize .fa-search-plus, #toggleImageSize.state-active .fa-search-minus {
  display: block;
}
.import-container {
  max-width: 700px;
  margin: inherit auto;
}
.imagesorter-label {
  float: left;
  width: 49.5%;
  width: calc(50% - 6px);
  text-align: center;
  text-transform: uppercase;
  font-size: 12px;
  background-color: #fff;
  color: #000;
  padding: 4px;
  border: 1px solid #d2d6de;
}
.imagesorter-label.label-active {
  background-color: #2C3B41;
  color: #fff;
  border: 1px solid #2C3B41;
}
.imagesorter-label:nth-child(2) {
  float: right;
}
.isItem {
  float: left;
  width: 120px;
  height: 150px;
  margin: 6px 6px 0 0;
  transition: width 200ms, height 200ms;
}
.isItem img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.isItem.sortable-ghost img {
  box-shadow: 0 0 2px 3px #D3EBFF inset, 0 0 2px 2px #7FBDEF;
}
.imagesize-big .isItem {
  width: 200px;
  height: 250px;
}
span.fake {
  color: #e99;
  margin-right: 6px;
}
</style>


<template>
  <div class="sorter-container labels clearfix">
    <div class="imagesorter-label">Available</div>
    <div class="imagesorter-label label-active">Use</div>
  </div>

  <div v-bind:class="{ 'imagesize-big': largeImages }" class="sorter-container zones">
    <div class="imagesorter-store" id="tagged_images-store">
      <div v-for="image in availableImages" class="isItem" data-id="{{ image.src }}">
        <img v-bind:src="image.src | image '400x400'" title="{{ image.tags != '' ? image.tags + ' | ' : '' }}{{ image.src }}" data-toggle="tooltip" data-placement="bottom" data-delay="500" data-original="{{ image }}">
      </div>
    </div>
    <div class="imagesorter-target" id="tagged_images-target" >
      <div v-for="image in product.tagged_images" class="isItem" data-id="{{ image.src }}">
        <img v-bind:src="image.src | image '400x400'" title="{{ image.tags != '' ? image.tags + ' | ' : '' }}{{ image.src }}" data-toggle="tooltip" data-placement="bottom" data-delay="500" data-original="{{ image }}">
      </div>
    </div>
    <div class="icon">
      <i class="fa fa-caret-left"></i>
      <i class="fa fa-caret-right"></i>
    </div>
  </div>

  <button v-on:click="toggleImageSize" v-bind:class="{ 'state-active': largeImages }" class="toggleImageSize" id="toggleImageSize" title="Toggle image size">
    <i class="fa fa-search-plus"></i>
    <i class="fa fa-search-minus"></i>
  </button>
</template>


<script>
import $ from 'jquery'
import Sortable from 'sortablejs'
import store from '../store'

const { toggleImageSize, loadStoreImages, updateProduct } = store.actions

export default {
  name: 'imagesorter',
  computed: {
    product() {
      return store.state.product
    },

    largeImages() {
      return store.state.largeImages
    },

    availableImages() {
      let images = []
      for(let im of store.state.storeImages) {
        var imgExists = false
        for (let xim of store.state.product.tagged_images) {
          if (xim.src == im.src) imgExists = true
        }
        if (!imgExists) {
          images.push(im)
        }
      }
      return images
    }
  },

  methods: {
    toggleImageSize,
  }, // end methods

  created() {
    loadStoreImages()
  },

  ready() {
    // setup sortables
    let storeSortable = new Sortable($('#tagged_images-store')[0], {
      draggable: '.isItem',
      group: {
        name: 'store',
        pull: true,
        put: ['store', 'target']
      },
      store: {
        get() {
          return []
        },
        set() {
          var storeImages = store.state.storeImages
          var tS = targetSortable.toArray()
          var newS = []
          tS.forEach((src) => {
            var original = $.grep(storeImages, (obj) => {
              return obj.src == src
            })
            if (original[0]) newS.push(original[0])
          })
          updateProduct({tagged_images: newS})
        }
      },
      sort: false,
    })

    let targetSortable = new Sortable($('#tagged_images-target')[0], {
      draggable: '.isItem',
      group: {
        name: 'target',
        pull: true,
        put: ['store', 'target']
      },
      store: {
        get() {
          return []
        },
        set() {
          var storeImages = store.state.storeImages
          var tS = targetSortable.toArray()
          var newS = []
          tS.forEach((src) => {
            var original = $.grep(storeImages, (obj) => {
              return obj.src == src
            })
            if (original[0]) newS.push(original[0])
          })
          updateProduct({tagged_images: newS})
        }
      },
    })
  }
}

</script>