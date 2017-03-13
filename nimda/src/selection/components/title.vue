<template>{{ selection.name }}</template>

<script>
import store from '../store'


export default {
  computed: {
    selection() {
      return store.state.selection
    }
  }
}
</script>