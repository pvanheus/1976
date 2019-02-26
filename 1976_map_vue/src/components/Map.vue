<template>
  <l-map ref="map" id="map" :zoom="zoom" :options=extraOptions :center="center">
    <l-tile-layer :url="url" :attribution="attribution" />
    <DeathMarker :key="death.person" v-for="death in deaths" :death="death" />
  </l-map>
</template>
<script>
import { LMap, LTileLayer, L } from 'vue2-leaflet'
import axios from 'axios'
import DeathMarker from './DeathMarker'

export default {
  name: 'Map',
  data() {
    return {
      // eslint-disable-next-line
      marker: L.latLng(-33.782221, 20.121103),
      deaths: null,
      zoom: 10,
      extraOptions: { zoomControl: false },
      // center: L.latLng(-28.8097176, 24.6074293),
      // eslint-disable-next-line
      center: L.latLng(-33.8881, 18.6726),
      url: 'https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=3b21bd0fa0114d6f8e27516bd47a7b20',
      // url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors & <a href="http://thunderforest.com/">Thunderforest</a>'
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
    });
    this.$nextTick( () => {
      this.map = this.$refs.map.mapObject;
      // eslint-disable-next-line
      alert(L.control.browserPrint);
      L.control.browserPrint().addTo(this.map);
    });
  }
}
</script>

<style scoped>
#map {
  width: 800px;
  height: 700px;
}
</style>
