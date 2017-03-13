const mutations = {
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
}

export default mutations