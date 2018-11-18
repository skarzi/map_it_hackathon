<template>
  <q-page class="flex flex-center text-center">
    <div class="row fullscreen container items-start">
      <div class="col-xs-12 header">
        <img class="logo" src="~assets/logo.png" alt="OnTime">
      </div>
      <div class="col-xs-12 form-contaier">
        <div class="row">
          <div class="offset-xs-3 col-xs-6 q-mt-md">
            <HereAutocomplete
              labelURL="assets/from.png"
              placeholder="From"
              v-model="fromLocation"
            />
          </div>
          <div class="offset-xs-3 col-xs-6 q-mt-md">
            <HereAutocomplete
              labelURL="assets/to.png"
              placeholder="To"
              v-model="toLocation"
            />
          </div>
          <div class="col-xs-12 q-mt-lg">
            <q-btn
              type="submit"
              label="Find Connection"
              color="secondary"
              size="lg"
              class="submit-button q-px-xl q-py-lg"
              full-width
            />
          </div>
        </div>
      </div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
      <div class="col-xs-12"></div>
    </div>
  </q-page>
</template>

<script>
import HereAutocomplete from '../components/HereAutocomplete.vue'

export default {
  name: 'PageIndex',
  components: {
    HereAutocomplete
  },
  data () {
    return {
      fromLocation: {},
      toLocation: {}
    }
  }
}
</script>

<style lang="stylus" scoped>
.q-layout-page
  background-color #30444d

.container
  background-color white
  margin-left 12%
  margin-right 12%

.header
  background-color #00bfa5
  height 150px

.logo
  height 75px
  top 50%
  transform translateY(50%)

.submit-button
  background-color #00bfa5
  border-radius 25px
</style>
