<style lang="sass">
  .list {
    background: #f4f4f4;
    overflow: hidden;
    padding: 8px 4px;
    &.four-cols {
      max-width: 840px;
    }
    .add {
      overflow: hidden;
      margin: 4px 4px 8px;
      .add-product {
        width: 408px;
      }
      .select2 {
        width: 408px!important;
      }
      .add-by-input {
        width: 407px !important;
        margin-left: 5px;
        margin-bottom: 10px;
        display: inline-block;
        vertical-align: top;
        height: 34px;
      }
      .add-by-input-button {
        border-radius: 2px;
        border: none;
        height: 34px;
        margin-left: 6px;
        padding-left: 16px;
        padding-right: 16px;
      }
    }
  }
  .products-list {
    li {
      float:left;
      width: 200px;
      height: 330px;
      overflow: hidden;
      border: 1px solid #e4e4e4;
      margin: 4px;
      position: relative;
      background: #fff;
      cursor: move;
      border-radius: 2px;
      &.inactive {
        > .image {
          opacity: 0.4;
        }
        > .title {
          color: #aaa;
          font-weight: normal;
          span {
            color: #e36d00;
          }
        }
        > .sku {
          font-weight: normal;
        }
      }
      img {
        width: 100%;
        display: block;
      }
      .image {
        height: 0;
        padding-bottom: 120%;
        background-size: contain;
        background-repeat: no-repeat;
        margin: 15px 12px 10px;
        &.empty {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          background: #eee;
        }
      }
      .title,
      .sku {
        display: block;
        text-align: center;
        font-weight: bold;
        font-size: 12px;
        line-height: 16px;
        padding: 0 10px;
      }
      .sku {
         color: #aaa;
      }
      .actionButton {
        background: #3c8dbc;
        cursor: pointer;
        position: absolute;
        top: 10px;
        color: #fff;
        font-weight: bold;
        font-size: 16px;
        height: 24px;
        line-height: 23px;
        width: 24px;
        text-align: center;
        border-radius: 2px;
        display: none;
        &:hover {
          background: #222!important;
        }
        &.deleter {
          background: #ea515f;
          right: 10px;
        }
        &.linker {
          right: 40px;
          font-size: 12px;
        }

        i {
          color: #fff;
        }
      }
      &.hover {
        border-color: #aaa;
        .actionButton {
          display: block;
        }
      }
      &.ghost {
        .actionButton {
          opacity: 0.2;
        }
      }
    }
  }
</style>
<template>
  <div class="list">
    <div className="inputs">
      <div class="add">
        <select class="add-product form-control"></select>
        <textarea class="add-by-input form-control" placeholder="Type 1 or more SKUs and press enter"></textarea>
        <button class="btn btn-primary btn-flat add-by-input-button">Add</button>
      </div>
    </div>
    <ul v-if="ready" class="products-list">
      <li v-for="(index, item) in items" track-by="$index" class="{{item.className}}">
        <div class="image" v-bind:style="{backgroundImage:'url('+item.image+')'}"></div>
        <div v-if="!item.image" class="image empty"></div>
        <span class="title">{{{ item.name }}}</span>
        <span class="sku">{{ item.sku }}</span>
        <span v-if="item.editUrl" class="actionButton linker"><a v-bind:href="item.editUrl"><i class="ion-edit"></i></a></span>
        <span class="actionButton deleter" data-index="{{index}}" v-on:click="remove">×</span>
      </li>
    </ul>
  </div>
</template>

<script>
import store from '../store'
import notie from '../../notie'
import $ from 'jquery'
import _ from 'underscore'
import Sortable from 'sortablejs'

const { updateSelection } = store.actions

const getImageByTag = (images, tag) => {
  // OBS: exists in utils too
  var image = _.find(images, (image) => {
    return image.tags.indexOf(tag) > -1
  })

  if (!image) {
    if (tag == 'primary') {
      image = images[0]
    } else if (tag == 'flatshot') {
      image = images[images.length - 1]
    } else if (tag == 'hover') {
      image = false
    } else {
      image = images[1] || images[0]
    }
  }

  return image ? '/media/'+image.src : '' //.replace(/\.(\w{3,4})$/,'_800x800.$1') : ''

}

export default {
  computed: {
    foo() {
      return 'FOO'
    }
  },
  methods: {
    remove(e) {
      var index = parseInt(e.currentTarget.getAttribute('data-index'), 10)
      var products = this.getProducts()
      if ( isNaN(index) ) {
        console.warn('Index "'+index+'" is not valid.')
      }
      products.splice(index, 1)
      var $listNode = $(e.currentTarget.parentNode)
      $listNode.animate({ opacity: 0 }, 200, () => {
        $listNode.animate({ width: 0 }, 200, () => {
          updateSelection({ products: products })
          this.updateItems()
          $listNode.removeAttr('style')
        })
      })
    },
    getProducts() {
      return store.state.selection.products.slice(0)
    },
    bulkAdd() {
      var $input = $('.add-by-input')
      var skus = $input.val().split(',').map((val) => val.trim()).filter((val) => {
        return val !== ''
      })
      if (skus.length > 0) {
        this.addProducts(skus)
        setTimeout(() => {
          $input.val('').focus()
        }, 4)
      }
    },
    addProducts(skus) {
      if ( !skus || !skus.length ) {
        return console.warn('Could not add skus: '+JSON.stringify(skus))
      }
      var valid = []
      var invalid = []
      skus.forEach((sku) => {
        if ( this.products[sku] ) {
          valid.push(sku)
        } else {
          invalid.push(sku)
        }
      })
      if ( invalid.length ) {
        notie.alert(3, 'The following SKUs where invalid: '+invalid.join(', '), 3)
      }
      if ( valid.length ) {
        var all = this.getProducts()
        var dups = _.intersection(all, valid)
        var done = () => {
          updateSelection({ products: valid.concat(all) })
          this.updateItems()
        }
        if ( dups.length ) {
          if ( window.confirm('The following products are already in the selection: \n\n'+(dups.join(', '))+'\n\nContinue?') ) {
            done()
          }
        } else {
          done()
        }
      }
    },
    createProduct(sku) {
      var product = this.products[sku]
      if ( !product ) {
        return {
          name: '<span>Not found:</span> '+sku,
          className: 'not-found',
          sku: sku
        }
      }
      product = Object.assign({}, product)
      if ( !product.isActive ) {
        product.name = '<span>Inactive: </span>'+product.name
        return Object.assign({ className: 'inactive' }, product)
      }

      return Object.assign({ className: '' }, product)
    },
    updateItems() {
      this.items = store.state.selection.products.map(this.createProduct)
    }
  },
  data() {
    return {
      items: [],
      products: {},
      ready: false
    }
  },
  created() {
    $.ajax({
      url: '/admin/api/products?all'
    }).done((res) => {
      res.products.forEach((p) => {
        this.products[p.sku] = {
          name: p.name,
          image: getImageByTag(p.tagged_images, 'primary'),
          isActive: p.is_active,
          sku: p.sku,
          editUrl: '/admin/products/product/' + p.id,
        }
      })
      this.ready = true
      this.updateItems()
      this.$nextTick(() => {
        var el = $('.products-list').get(0)
        var sortable = new Sortable(el, {
          animation: 200,
          onStart: (e) => {
            $('li.hover').removeClass('hover')
          },
          onEnd: (e) => {
            var products = this.getProducts()
            var sliced = products.splice(e.oldIndex, 1)
            if ( !sliced[0] ) {
              return console.warn('Product at index '+e.oldIndex+' could not be removed.')
            }
            products.splice(e.newIndex, 0, sliced[0])
            updateSelection({ products: products })
            this.updateItems()
          },
          onUpdate: (e) => {
            $('li.hover').removeClass('hover')
          }
        })
      })
    })
  },
  ready() {
    var $addProduct = $('.add-product').select2({
      ajax: {
        url: "/admin/api/productsearch/",
        dataType: 'json',
        cache: true,
        processResults: (data, params) => {
          data.results.forEach((item) => {
            item.text = item.name
            item.id = item.sku
          })
          return data
        }
      },
      minimumInputLength: 1,
      placeholder: 'Search & add a single product',
    }).on('change', (e) => {
      var value = $(e.target).find(':selected').val()
      if ( value ) {
        this.addProducts([value])
        $addProduct.val('').trigger('change')
      }
    })
    $('.list').on('mouseenter', 'li', (e) => {
      $(e.currentTarget).addClass('hover')
    }).on('mouseleave' ,'li', (e) => {
      $(e.currentTarget).removeClass('hover')
    })
    $('.add-by-input').on('keypress', (e) => {
      if ( e.which == 13 && e.target.value ) {
        e.preventDefault()
        this.bulkAdd()
      }
    })
    $('.add-by-input-button').on('click', () => {
      this.bulkAdd()
    })
  }
}
</script>