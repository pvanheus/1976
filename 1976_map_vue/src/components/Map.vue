<template>
  <l-map id="map" :zoom="zoom" :center="center">
    <l-tile-layer :url="url" :attribution="attribution" />
    <DeathMarker :key="death.person" v-for="death in deaths" :death="death" />
  </l-map>
</template>
<script>
import { LMap, LTileLayer } from 'vue2-leaflet'
import axios from 'axios'
import DeathMarker from './DeathMarker'

export default {
  name: 'Map',
  data() {
    return {
      // eslint-disable-next-line
      marker: L.latLng(-33.782221, 20.121103),
      deaths: null,
      zoom: 6,
      // eslint-disable-next-line
      center: L.latLng(-28.8097176, 24.6074293),
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }
  },
  components: {
    DeathMarker,
    LMap,
    LTileLayer
  },
  mounted() {
    axios.get('https://raw.githubusercontent.com/pvanheus/1976/master/1976_deaths.json').then(response => {
      this.deaths = response.data
    })
  }
}
</script>

<style scoped>
#map {
  width: 800px;
  height: 700px;
}
</style>
