import $ from 'jquery'
import './image-picker.js' // register image picker plugin
import './image-picker.css'
import './product.scss'


export default {
  type: 'product',

  icon_name: 'ion-cube',

  title() { return 'Product' },

  loadData(data, options) {
    let $editor = $(this.editor)

    $.ajax({
      url: `/admin/api/productimages/${data.product}/`,
      context: this
    }).done(function (p) {
      let $product = $editor.find('.product')
      $product.append(`<option value="${data.product}">${p.name}</option>`)
      $product.select2({
        ajax: {
          url: "/admin/api/productsearch/",
          dataType: 'json',
          cache: true
        },
        minimumInputLength: 1,
      })
      $editor.find('.images').html('<select></select>')
      let $imagesSelect = $editor.find('.images select')
      for (let im of p.images) {
        im = im.src
        let attrs = data.image == im ? 'selected="selected" ' : ''
        let name = im
        let lastDot = im.lastIndexOf('.')
        if (lastDot > 0) {
          name = im.substring(0, lastDot)
        }
        let imageUrl = `/${name}_100x100.jpg`
        let label = ''
        if (name.match(/img\/ys_/)) {
          label = 'YS'
        }
        $imagesSelect.append(`<option ${attrs}data-img-src="${imageUrl}" data-img-label="${label}" value="${im}"></option>`)
      }
      if (options && options.showImages) {
        this.toggleImages()
      }
    })
  },

  save() {
    let $editor = $(this.editor)
    let product = $editor.find('.product').find(':selected').val()
    let image = $editor.find('.images select').find(':selected').val()
    let data = {
      product: product,
      image: image
    }
    if (product) {
      this.setData(data)
    }
  },

  editorHTML: `
  <div class="st-block__editor">
    <div class="col-md-6">
      <select class="product"></select>
    </div>
    <div class="col-md-6">
      <button class="btn-loadimages btn btn-flat btn-default">Toggle images</button>
    </div>
    <div class="box-body images state-inactive">
    </div>
  </div>`,

  toggleImages() {
    let $editor = $(this.editor)
    $editor.find('.images').toggleClass('state-inactive')
    $editor.find('.images select').imagepicker({show_label: true})
  },

  onBlockRender() {
    let $editor = $(this.editor)
    let $product = $editor.find('.product')

    $editor.find('.btn-loadimages').on('click', () => {
      this.toggleImages()
    })

    $product.select2({
      ajax: {
        url: "/admin/api/productsearch/",
        dataType: 'json',
        cache: true
      },
      minimumInputLength: 1,
    }).on('change', (e) => {
      let data = {
        'product': $(e.target).find(':selected').val()
      }
      this.loadData(data, {showImages: true})
    })
  }

}
