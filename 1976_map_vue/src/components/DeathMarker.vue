<template>
  <l-circle-marker
          v-if="latLng && visible"
          :lat-lng="latLng"
          :radius="markerRadius"
          :color="markerColour"
  >
    <l-popup>
      <DeathPopupContent :death="death" />
    </l-popup>
  </l-circle-marker>
</template>

<script>
import { LCircleMarker, LPopup } from 'vue2-leaflet'
import DeathPopupContent from './DeathPopupContent'

export default {
  name: 'DeathMapMarker',
  props: {
    death: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      visible: true,
      markerRadius: 3,
      markerColour: "#FF0000"
    }
  },
  computed: {
    latLng() {
      if (this.death) {
        // eslint-disable-next-line
        return L.latLng(this.death.latitude, this.death.longitude)
      } else {
        return null
      }
    }
  },
  components: { DeathPopupContent, LCircleMarker, LPopup }
}
</script>

<style scoped>
</style>
