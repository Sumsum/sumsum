<style lang="sass">
  .save-top {
    height: 34px;
  }
  .form-group .select2 {
    width: 100% !important;
  }
  .reload-btn {
    margin-right: 20px;
  }
</style>

<template>
    <div class="margin-bottom save-top">
      <a v-if="selection.id" class="btn btn-default btn-flat" href="../delete/">Delete</a>
      <a class="btn btn-primary pull-right btn-flat" v-on:click="save">Save</a>
      <a class="reload-btn btn btn-default pull-right btn-flat" v-on:click="saveAndReload">Save & Reload</a>
    </div>
    <div class="box">
      <div class="box-body">
        <div class="row">
          <div class="col-md-12">
            <a class="toggle-fourcols-btn btn btn-default pull-right btn-flat" v-on:click="toggleFourCols">4 columns</a>
            <a class="toggle-inactive-btn btn btn-default pull-right btn-flat" v-on:click="toggleInactive">Toggle inactive</a>
            <!-- <a class="btn btn-flat btn-default pull-right" href="/selection/{{ selection.slug }}?preview=✓" target=_blank>Preview</a> -->
          </div>
        </div>
        <div class="row">

          <div class="col-md-6">
            <div class="form-group">
              <label class="required" for="id_name">Name</label>
              <input :value="selection.name" @input="updateName" class="form-control" id="id_name" maxlength="500" name="name" type="text">
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label class="required" for="id_slug">Slug</label>
              <input :value="selection.slug" @input="updateSlug" class="form-control" id="id_slug" maxlength="500" name="slug" type="text">
            </div>
          </div>

        </div>

        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="id_categorysync">Category Sync.</label>
              <select id="id_categorysync" class="form-control" :selected="selection.category"></select>
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label for="id_fitsync">Fit Sync.</label>
              <select id="id_fitsync" class="form-control" :selected="selection.fit"></select>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="id_description">Description</label>
              <textarea :value="selection.description" @input="updateDescription" class="form-control" cols="40" id="id_description" name="description" rows="5"></textarea>
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label for="id_visible">Visible</label>
              <input v-model="selection.visible" @click="updateVisible" class="checkbox" id="id_visible" name="visible" type="checkbox">
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <products></products>
            </div>
          </div>
        </div>

      </div>
    </div>
    <div class="clearfix">
      <a class="btn btn-default btn-flat" href="../delete/" v-if="selection.id">Delete</a>
      <a class="btn btn-primary pull-right btn-flat" v-on:click="save">Save</a>
      <a class="reload-btn btn btn-default pull-right btn-flat" v-on:click="saveAndReload">Save & Reload</a>
    </div>
</template>


<script>
import store from '../store'
import Urlify from 'urlify'
import notie from '../../notie'
import $ from 'jquery'

const { loadInitialSelection, updateSelection, setSelectionAutoSlug, saveSelection } = store.actions
const urlify = Urlify.create({
  spaces: '-',
  nonPrintable: '-',
  toLower: true,
  trim: true
})
// fixes å
const slugify = (s) => {
  s = s.replace(/å/gi, 'a')
  return urlify(s)
}

export default {

  computed: {
    selection() {
      return store.state.selection
    },
    selectionAutoSlug() {
      return store.state.selectionAutoSlug
    }
  },

  methods: {
    save(options) {
      if(!this.selection.name) {
        notie.alert(3, 'Missing name', 3)
        $('#id_name').focus()
        $('#id_name').css('border', '1px red solid')
        setTimeout(() => { $('#id_name').css('border', '1px rgb(210, 214, 222) solid') }, 2000)
        return
      }
      if(!this.selection.slug) {
        notie.alert(3, 'Missing slug', 3)
        $('#id_slug').focus()
        $('#id_slug').css('border', '1px red solid')
        setTimeout(() => { $('#id_slug').css('border', '1px rgb(210, 214, 222) solid') }, 2000)
        return
      }
      // console.log('saving', options)
      saveSelection(options)
    },

    saveAndReload() {
      this.save({reload: true})
    },

    toggleInactive() {
      $('.products-list li.inactive').toggle()
      if ($('.toggle-inactive-btn').hasClass('active')) {
        $('.toggle-inactive-btn').removeClass('active')
      } else {
        $('.toggle-inactive-btn').addClass('active')
      }
    },

    toggleFourCols() {
      let $list = $('.list')
      if ($list.hasClass('four-cols')) {
        $list.removeClass('four-cols')
        $('.toggle-fourcols-btn').removeClass('active')
      } else {
        $list.addClass('four-cols')
        $('.toggle-fourcols-btn').addClass('active')
      }
    },

    updateName(e) {
      let name = e.target.value
      let data = {name: name}
      if(this.selectionAutoSlug) {
        data.slug = slugify(name)
      }
      updateSelection(data)
    },

    updateSlug(e) {
      setSelectionAutoSlug(!e.target.value)
      updateSelection({slug: slugify(e.target.value)})
    },

    updateDescription(e) {
      updateSelection({description: e.target.value})
    },

    updateVisible(e) {
      updateSelection({visible: e.target.checked})
    },

  },

  created() {
    loadInitialSelection()
  },

  ready() {

    $.ajax({
      url: '/admin/api/categorychoices/'
    }).done((res) => {
      let $categorySync = $('#id_categorysync')
      $categorySync.select2({
        data: res.results
      })
      $categorySync.val(store.state.selection.category).trigger('change')
      $categorySync.on('select2:select', (e) => { updateSelection({category: e.params.data.id }) })
    })

    $.ajax({
      url: '/admin/api/fitchoices/'
    }).done((res) => {
      let $fitSync = $('#id_fitsync')
      $fitSync.select2({
        data: res.results,
      })
      $fitSync.val(store.state.selection.fit).trigger('change')
      $fitSync.on('select2:select', (e) => { updateSelection({fit: e.params.data.id }) })
    })

  }

}
</script>
