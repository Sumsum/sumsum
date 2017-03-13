<template>
  <div class="row">
    <div class="col-md-4">
      <div class="box box-warning collapsed-box">
        <div class="box-header">
          <h3 class="box-title">Cache</h3>
          <div class="box-tools pull-right">
            <button class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-plus"></i></button>
          </div>
        </div>
        <div class="box-body">
          <button @click="wipeGlobals" :disabled="globals.disabled" type="button" class="btn btn-{{ globals.btn }} btn-block btn-flat">{{ globals.msg }} <i style="float:right" :class="globals.iconClass"></i></button>
          <button @click="updateReactData" data-target="home" :disabled="reactData.disabled" type="button" class="btn btn-{{ reactData.btn }} btn-block btn-flat">{{ reactData.msg }} <i style="float:right" :class="reactData.iconClass"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  const initialGlobals = {
    msg: 'Wipe Customdata cache',
    btn: 'default',
    iconClass: '',
    disabled: false
  }

  const initialReactData = {
    msg: 'Update home page cache',
    btn: 'default',
    iconClass: '',
    disabled: false
  }

  export default {
    data() {
      return {
        globals: initialGlobals,
        reactData: initialReactData,
      }
    },
    methods: {
      ///////
      wipeGlobals() {
        this.globals = {
          msg: 'Wait, wiping customdata',
          btn: 'default',
          iconClass: 'ion-load-c ion-spin-animation',
          disabled: true
        }

        $.ajax({
          context: this,
          url: '/admin/api/wipeglobals/'
        }).done(() => {
          this.globals = {
            msg: 'Done wiping customdata',
            btn: 'success',
            iconClass: '',
            disabled: true
          }

          setTimeout(() => {
            this.globals = initialGlobals
          }, 1500)
        })
      },

      ///////
      updateReactData(e) {
        let el = e.currentTarget
        let target = $(el).attr('data-target')
        this.reactData = {
          msg: 'Wait, updating cache for ' + (target == 'nostores' ? ' all but stores' : target),
          btn: 'default',
          iconClass: 'ion-load-c ion-spin-animation',
          disabled: true
        }

        $.ajax({
          context: this,
          url: '/admin/api/updatereactdata/' + target + '/',
          // This is not working, timeouts are set in multiple places
          // Trigger job and poll progress instead?
          // http://www.dangtrinh.com/2013/07/django-celery-display-progress-bar-of.html
          // http://sunshineatnoon.github.io/How-to-create-a-progressbar-in-Django/
          // http://killtheyak.com/django-celery-redis/
          // timeout: 240000, // Four minutes. Whoa!
          // async: true,
        }).done(() => {
          this.reactData = {
            msg: 'Done updating cache',
            btn: 'success',
            iconClass: '',
            disabled: true
          }

          setTimeout(() => {
            this.reactData = initialReactData
          }, 1500)
        })
      },
    }
  }

</script>
