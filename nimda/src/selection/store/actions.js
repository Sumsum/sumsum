import $ from 'jquery'
import _ from 'lodash'
import notie from '../../notie'
import Cookies from 'js-cookie'
import SirTrevor from '../../sirtrevor'
import Vue from 'vue'


const pkMatch = location.pathname.match(/\/([^\/]+)\/change\/$/)
const pk = pkMatch ? pkMatch[1] : 'none'
const selectionApi = `/admin/products/selection/${pk}/api/`
const selectionAddApi = `/admin/products/selection/api/add/`


export const loadInitialSelection = (store) => {
  if(window.original) {
    store.dispatch('SET_SELECTION', _.cloneDeep(window.original))
  } else {
    store.dispatch('SET_SELECTION', {
      name: '',
      slug: '',
      description: '',
      visible: true,
      category: '',
      fit: '',
      filters: [],
      products: [],
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

export const saveSelection = (store, options) => {
  let fields = ['name', 'slug', 'category', 'fit', 'filters', 'visible', 'description', 'products']
  let data = _.pick(store.state.selection, fields)
  console.log('SAVING', fields, data)
  data.fit = data.fit ? parseInt(data.fit) : null
  if (pkMatch) {
    console.log('AJAX', JSON.stringify(data), selectionApi)
    $.ajax({
      url: selectionApi,
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      method: 'PUT',
      data: JSON.stringify(data)
    }).done((res) => {
      if (options && options.reload) {
        location.reload()
      } else {
        notie.alert(1, 'Selection updated', 2)
      }
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