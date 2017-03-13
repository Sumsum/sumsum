import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'
import mutations from './mutations'


Vue.use(Vuex)


const state = {
  // product
  product: {},
  largeImages: false,
  storeImages: [],
}

export default new Vuex.Store({
  state,
  mutations,
  actions,
  strict: true
})