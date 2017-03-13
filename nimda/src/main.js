'use strict'

import './adminlte'
import './init'
import './django'

import Vue from 'vue'
Vue.config.debug = true


Vue.component('index-load', require('./index/components/load.vue'))
Vue.component('index-cache', require('./index/components/cache.vue'))

Vue.component('product', require('./product/components/product.vue'))
Vue.component('product-image-sorter', require('./product/components/image-sorter.vue'))
Vue.component('product-dropzone', require('./product/components/dropzone.vue'))
Vue.component('product-sir-trevor', require('./product/components/sirtrevor.vue'))

Vue.component('selection', require('./selection/components/selection.vue'))
Vue.component('selection-title', require('./selection/components/title.vue'))
Vue.component('products', require('./selection/components/products.vue'))

Vue.component('image-list-dropzone', require('./image-list/components/dropzone.vue'))


Vue.filter('stringify', (value) => {
  return JSON.stringify(value, null, '  ')
})

Vue.filter('image', (name, dim) => {
  // var name = obj.src
  let lastDot = name.lastIndexOf('.')
  if (lastDot > 0) {
    name = name.substring(0, lastDot)
  }
  // return {
  //   src: `/${name}_${dim}.jpg`,
  //   alt: obj.alt,
  //   tags: obj.tags,
  // }
  return `/${name}_${dim}.jpg`
})

Vue.filter('toString', (value) => {
  return typeof(value) === 'string' ? value : JSON.stringify(value)
})


new Vue({ el: 'body' })
