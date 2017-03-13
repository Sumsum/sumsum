const mutations = {
  // product
  TOGGLE_LARGE_IMAGES(state) {
    state.largeImages = !state.largeImages
  },
  SET_PRODUCT(state, product) {
    state.product = product
  },
  UPDATE_PRODUCT(state, data) {
    for(let attr in data) {
      state.product[attr] = data[attr]
    }
  },
  SET_STORE_IMAGES(state, storeImages) {
    state.storeImages = storeImages
  },

  // selection
  SET_SELECTION(state, selection) {
    state.selection = selection
  },
  UPDATE_SELECTION(state, data) {
    for(let attr in data) {
      state.selection[attr] = data[attr]
    }
  },
  SET_SELECTION_AUTO_SLUG(state, value) {
    state.selectionAutoSlug = !!value
  }
}

export default mutations