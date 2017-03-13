import $ from 'jquery'
import _ from 'lodash'
import notie from '../../notie'
import Cookies from 'js-cookie'


const pkMatch = location.pathname.match(/\/([^\/]+)\/change\/$/)
const pk = pkMatch ? pkMatch[1] : 'none'
const productApi = `/admin/products/product/${pk}/api/`
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

export const updateProductStore = (store, data) => {
  store.dispatch('UPDATE_PRODUCT', data)
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