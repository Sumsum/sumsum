<style lang="sass">
.attr {
  font-weight: bold;
  display: block;
}
#ys div {
  margin-bottom: 7px;
}
#ys pre {
  background-color: #fff;
  border: none;
  font-family: courier;
  font-size: 13px;
  padding: 0;
}
.product-save {
  margin-bottom: 20px;
}
.row.summary {
  margin-bottom: 10px;
}
.attributes div {
  margin-bottom: 7px;
}
.images-link {
  padding: 20px 0;
}
</style>


<template>
<div class="row">
  <div class="col-md-12">
    <div class="nav-tabs-custom">
      <ul class="nav nav-tabs">
        <li class="active"><a href="#summary" data-toggle="tab">Summary</a></li>
        <li><a href="#images" data-toggle="tab">Images</a></li>
        <li><a href="#ys" data-toggle="tab">Y/S</a></li>
      </ul>

      <div class="tab-content">
        <div class="active tab-pane" id="summary">
          <div class="product-save">
            <a v-on:click="save" class="btn btn-primary btn-flat">Save</a>
            <a class="btn btn-flat btn-default pull-right" href="/product/{{ product.uri }}?preview=✓" target=_blank>Preview</a>
          </div>
          <div class="row summary">
            <div class="col-md-6">
              <img v-if="firstImage" class="col-xs-12" v-bind:src="firstImage | image '600x800'" title="{{ firstImage }}" data-toggle="tooltip" data-placement="bottom" data-delay="500">
            </div>
            <div class="col-md-6 attributes">
              <div><span class="attr">Active </span><span>{{ product.is_active }}</span></div>
              <div><span class="attr">Name </span><span>{{ product.name }}</span></div>
              <div><span class="attr">Excerpt (short desc) </span><span>{{ product.excerpt }}</span></div>
              <div><span class="attr">Description (long desc) </span><span>{{ product.description }}</span></div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="id_name">Color</label>
                <input :value="product.color" @input="updateColor" class="form-control" id="id_color" maxlength="500" name="color" type="text">
              </div>
            </div>
          </div>
        </div>

        <div class="tab-pane" id="images">
          <div class="images-link"><a href="/admin/images/image/?pim=only&o=3.-5&q={{ product.sku }}">
            Edit images for this product
          </a></div>
          <product-image-sorter></product-image-sorter>
          <product-dropzone></product-dropzone>
        </div>

        <div class="tab-pane" id="ys">
          <div><span class="attr">Name </span><span>{{ product.name }}</span></div>
          <div><span class="attr">sku </span><span>{{ product.sku }}</span></div>
          <div><span class="attr">Description </span><span>{{ product.description }}</span></div>
          <div><span class="attr">Attributes </span><pre>{{ product.attributes|stringify }}</pre></div>
          <div><span class="attr">canonicalCategory </span><span>{{ product.canonicalCategory }}</span></div>
          <div><span class="attr">canonicalUri </span><span>{{ product.canonicalUri }}</span></div>
          <div><span class="attr">categories </span><pre>{{ product.categories|stringify }}</pre></div>
          <div><span class="attr">collection </span><span>{{ product.collection }}</span></div>
          <div><span class="attr">collectionName </span><span>{{ product.collectionName }}</span></div>
          <div><span class="attr">excerpt </span><span>{{ product.excerpt }}</span></div>
          <div><span class="attr">fit </span><span>{{ product.fit }}</span></div>
          <div><span class="attr">fit_group </span><span>{{ product.fit_group }}</span></div>
          <div><span class="attr">gender </span><span>{{ product.gender }}</span></div>
          <div><span class="attr">localized </span><span>{{ product.localized }}</span></div>
          <div><span class="attr">measurementChart </span><span>{{ product.measurementChart }}</span></div>
          <div><span class="attr">measurementChartRows </span><pre>{{ product.measurementChartRows|stringify }}</pre></div>
          <div><span class="attr">metaDescription </span><span>{{ product.metaDescription }}</span></div>
          <div><span class="attr">metaKeywords </span><span>{{ product.metaKeywords }}</span></div>
          <div><span class="attr">metaTitle </span><span>{{ product.metaTitle }}</span></div>
          <div><span class="attr">procurement_group </span><span>{{ product.procurement_group }}</span></div>
          <div><span class="attr">productSku </span><span>{{ product.productSku }}</span></div>
          <div><span class="attr">relatedProducts </span><pre>{{ product.relatedProducts|stringify }}</pre></div>
          <div><span class="attr">silkProduct </span><span>{{ product.silkProduct }}</span></div>
          <div><span class="attr">silkProductName </span><span>{{ product.silkProductName }}</span></div>
          <div><span class="attr">silkVariant </span><span>{{ productsilkVariant }}</span></div>
          <div><span class="attr">stockUnit </span><span>{{ product.stockUnit }}</span></div>
          <div><span class="attr">tags </span><pre>{{ product.tags|stringify }}</pre></div>
          <div><span class="attr">uri </span><span>{{ product.uri }}</span></div>
          <div><span class="attr">variantName </span><span>{{ product.variantName }}</span></div>
          <div><span class="attr">weight </span><span>{{ product.weight }}</span></div>
          <div><span class="attr">weightUnit </span><span>{{ product.weightUnit }}</span></div>
          <div><span class="attr">harmCode </span><span>{{ product.harmCode }}</span></div>
          <div><span class="attr">harmCodeDescription </span><span>{{ product.harmCodeDescription }}</span></div>
          <div><span class="attr">countryOfOrigin </span><span>{{ product.countryOfOrigin }}</span></div>
          <div><span class="attr">countryOfOriginName </span><span>{{ product.countryOfOriginName }}</span></div>
          <div><span class="attr">markets </span><pre>{{ product.markets|stringify }}</pre></div>
          <div><span class="attr">media </span><pre>{{ product.media|stringify }}</pre></div>
          <div><span class="attr">items </span><pre>{{ product.items|stringify }}</pre></div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>


<script>
import store from '../store'
const { loadInitialProduct, updateProductStore, updateProduct } = store.actions


export default {
  computed: {
    product() {
      return store.state.product
    },
    firstImage() {
      // TODO We should probably fetch the first image tagged as 'primary' here
      if (this.product.tagged_images.length) {
        return this.product.tagged_images[0] ? this.product.tagged_images[0].src : ''
      }
    }
  },
  created() {
    loadInitialProduct()
  },
  methods: {
    save() {
      updateProduct({
        color: store.state.product.color,
      })

    },
    updateColor(e) {
      updateProductStore({color: e.target.value})
    }
  }

}
</script>
