<template>
  <div class="row">
    <div class="col-md-4">
      <div class="box">
        <div class="box-header">
          <h3 class="box-title">Load data from Y/S Silk</h3>
        </div>
        <div class="box-body">
          <button @click="loadProducts" :disabled="products.disabled" type="button" class="btn btn-{{ products.btn }} btn-block btn-flat">{{ products.msg }} <i style="float:right" :class="products.iconClass"></i></button>
          <button @click="loadCategoryTrees" :disabled="categoryTrees.disabled" type="button" class="btn btn-{{ categoryTrees.btn }} btn-block btn-flat">{{ categoryTrees.msg }} <i style="float:right" :class="categoryTrees.iconClass"></i></button>
          <button @click="loadMarkets" :disabled="markets.disabled" type="button" class="btn btn-{{ markets.btn }} btn-block btn-flat">{{ markets.msg }} <i style="float:right" :class="markets.iconClass"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  const initialProducts = {
    msg: 'Load products',
    btn: 'default',
    iconClass: '',
    disabled: false
  }

  const initialCategoryTrees = {
    msg: 'Load category trees',
    btn: 'default',
    iconClass: '',
    disabled: false
  }

  const initialMarkets = {
    msg: 'Load markets',
    btn: 'default',
    iconClass: '',
    disabled: false
  }

  export default {
    data() {
      return {
        products: initialProducts,
        categoryTrees: initialCategoryTrees,
        markets: initialMarkets,
      }
    },

    methods: {
      ///////
      loadProducts() {
        this.products = {
          msg: 'Wait, loading products',
          btn: 'default',
          iconClass: 'ion-load-c ion-spin-animation',
          disabled: true
        }

        $.ajax({
          context: this,
          url: '/admin/api/loadproducts/'
        }).done(() => {
          this.products = {
            msg: 'Done loading products',
            btn: 'success',
            iconClass: '',
            disabled: true
          }

          setTimeout(() => {
            this.products = initialProducts
          }, 1500)
        })
      },

      ///////
      loadCategoryTrees() {
        this.categoryTrees = {
          msg: 'Wait, loading category trees',
          btn: 'default',
          iconClass: 'ion-load-c ion-spin-animation',
          disabled: true
        }

        $.ajax({
          context: this,
          url: '/admin/api/loadcategorytrees/'
        }).done(() => {
          this.categoryTrees = {
            msg: 'Done loading category trees',
            btn: 'success',
            iconClass: '',
            disabled: true
          }

          setTimeout(() => {
            this.categoryTrees = initialCategoryTrees
          }, 1500)
        })
      },

      ///////
      loadMarkets() {
        this.markets = {
          msg: 'Wait, loading markets',
          btn: 'default',
          iconClass: 'ion-load-c ion-spin-animation',
          disabled: true
        }

        $.ajax({
          context: this,
          url: '/admin/api/loadmarkets/'
        }).done(() => {
          this.markets = {
            msg: 'Done loading markets',
            btn: 'success',
            iconClass: '',
            disabled: true
          }

          setTimeout(() => {
            this.markets = initialMarkets
          }, 1500)
        })
      },
    }
  }
</script>
