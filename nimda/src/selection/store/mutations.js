const mutations = {
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