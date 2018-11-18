<template>
  <div>
    <div class="row">
      <div class="col-xs-2">
        <img class="label-image" :src="labelURL">
      </div>
      <div class="col-xs-10">
        <q-input
          @focus="focusOnField"
          class="here-input"
          v-model="terms"
          :placeholder="placeholder"
          clearable
          hide-underline
        >
          <q-autocomplete
            @search="searchPlace"
            :min-characters="3"
            :max-results="10"
            @selected="selectPlace"
          />
        </q-input>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HereAutocomplete',
  data () {
    return {
      terms: '',
      suggestions: []
    }
  },
  props: {
    value: Object,
    labelURL: String,
    placeholder: String
  },
  methods: {
    focusOnField (event) {
      console.log(event.relatedTarget)
    },
    async searchPlace (terms, done) {
      console.log('searching for', terms)
      try {
        let response = await this.$axios.get(
          'http://autocomplete.geocoder.api.here.com/6.2/suggest.json',
          {
            params: {
              app_id: 'Lw639bgCPrd9dTnBfJsF',
              app_code: 'Lyhc0GQGSkaTQtsa0WxyKw',
              country: 'POL',
              language: 'pl',
              maxresults: 10,
              query: terms,
              beginHighlight: '<b>',
              endHighlight: '</b>'
            }
          }
        )
        let suggestions = response.data.suggestions.map((suggestion) => {
          return {
            label: suggestion.label,
            value: suggestion.label.replace(/<\/?[^>]+(>|$)/g, ''),
            locationID: suggestion.locationId
          }
        })
        console.log(suggestions)
        done(suggestions)
      } catch (error) {
        console.log(error)
        done([])
      }
    },
    async selectPlace (item) {
      console.log('selected', item)
      try {
        let response = await this.$axios.get(
          'http://geocoder.api.here.com/6.2/geocode.json',
          {
            params: {
              app_id: 'Lw639bgCPrd9dTnBfJsF',
              app_code: 'Lyhc0GQGSkaTQtsa0WxyKw',
              locationid: item.locationID,
              jsonattributes: 1,
              gen: 9
            }
          }
        )
        let position = response.data.response.view[0].result[0].location.displayPosition
        this.$emit('input', position)
      } catch (error) {
        console.log(error)
      }
    }
  },
  mounted () {
    if (Object.keys(this.value).length !== 0) {
      this.$axios(
        'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json',
        {
          params: {
            app_id: 'Lw639bgCPrd9dTnBfJsF',
            app_code: 'Lyhc0GQGSkaTQtsa0WxyKw',
            gen: 9,
            language: 'pl',
            mode: 'retrieveAddresses',
            prox: `${this.value.latitude},${this.value.longitude}`
          }
        }
      ).then((response) => {
        console.log(response)
        let data = response.data.Response.View[0].Result[0].Location
        this.terms = data.Address.Label
        this.$emit('input', {
          latitude: data.DisplayPosition.Latitude,
          longitude: data.DisplayPosition.Longitude
        })
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.label-image
  height 35px

.here-input
  border-radius 25px
  border solid 1px #cccccc
  padding 10px 20px
</style>
