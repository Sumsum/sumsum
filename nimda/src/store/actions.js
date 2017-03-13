import $ from 'jquery'
import _ from 'lodash'
import notie from '../notie'
import Cookies from 'js-cookie'


// product
const pkMatch = location.pathname.match(/\/([^\/]+)\/change\/$/)
const pk = pkMatch ? pkMatch[1] : 'none'
const productApi = `/admin/products/product/${pk}/api/`
const selectionApi = `/admin/products/selection/${pk}/api/`
const selectionAddApi = `/admin/products/selection/api/add/`
const productImagesApi = `/admin/api/productimages/${pk}/`


export const toggleImageSize = 'TOGGLE_LARGE_IMAGES'

export const loadInitialProduct = (store) => {
  store.dispatch('SET_PRODUCT', _.cloneDeep(window.original))
}

export const loadStoreImages = (store) => {
  $.get(productImagesApi).done((res) => {
    store.dispatch('SET_STORE_IMAGES', res.images)
  })
}

export const loadDetailImages = (store) => {
  $.get(productApi).done((res) => {
    store.dispatch('UPDATE_PRODUCT', {tagged_images: res.tagged_images})
    notie.alert(1, 'Product updated', 1)
  })
}

export const updateProduct = (store, data) => {
  store.dispatch('UPDATE_PRODUCT', data)
  $.ajax({
    url: productApi,
    headers: {'X-CSRFToken': Cookies.get('csrftoken')},
    method: 'PUT',
    data: JSON.stringify(data)
  }).done(() => {
    notie.alert(1, 'Product updated', 1)
  })
}

// selection
export const loadInitialSelection = (store) => {
  if(window.original) {
    store.dispatch('SET_SELECTION', _.cloneDeep(window.original))
  } else {
    store.dispatch('SET_SELECTION', {
      name: '',
      slug: '',
      description: '',
      filters: [],
      products: []
    })
    setSelectionAutoSlug(store, true)
  }
}

export const setSelectionAutoSlug = (store, value) => {
  store.dispatch('SET_SELECTION_AUTO_SLUG', !!value)
}

export const updateSelection = (store, data) => {
  store.dispatch('UPDATE_SELECTION', data)
}

export const saveSelection = (store) => {
  let fields = ['name', 'slug', 'filters', 'description', 'sirtrevor']
  let data = _.pick(store.state.selection, fields)
  if (pkMatch) {
    $.ajax({
      url: selectionApi,
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      method: 'PUT',
      data: JSON.stringify(data)
    }).done(() => {
      notie.alert(1, 'Selection updated', 1)
    })
  } else {
    $.ajax({
      url: selectionAddApi,
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      method: 'POST',
      data: JSON.stringify(data)
    }).done((res) => {
      // we need the id
      //store.dispatch('UPDATE_SELECTION', res)
      location = `../${res.id}/change/`
      //notie.alert(1, 'Selection saved', 1)
    })
  }
}