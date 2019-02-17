<template>
  <l-marker v-if="latLng && visible" :lat-lng="latLng">
    <l-popup>
      <DeathPopupContent :death="death" />
    </l-popup>
  </l-marker>
</template>

<script>
import { LMarker, LPopup } from 'vue2-leaflet'
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
      visible: true
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
  components: { DeathPopupContent, LMarker, LPopup }
}
</script>

<style scoped></style>
