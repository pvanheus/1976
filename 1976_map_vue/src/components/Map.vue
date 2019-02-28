<template>
  <l-map
          ref="map"
          id="map"
          :zoom="zoom"
          :options=extraOptions
          :center="center"
  >
    <l-tile-layer
            :url="url"
            :attribution="attribution"
    />
    <template v-if="deaths">
      <DeathMarker
              :key="death.person"
              v-for="death in deaths"
              :death="death"
      />
    </template>
    <!--<BrowserPrint/>-->
  </l-map>
</template>
<script>
import { LMap, LTileLayer, L } from 'vue2-leaflet'
import axios from 'axios'
import DeathMarker from './DeathMarker'
import 'leaflet-easyprint'
// import BrowserPrint from "./BrowserPrint";

export default {
  name: 'Map',
  data() {
    return {
      deaths: null,
      zoom: 10,
      extraOptions: { zoomControl: false },
      // center: L.latLng(-28.8097176, 24.6074293),
      // eslint-disable-next-line
      center: L.latLng(-33.8881, 18.6726),
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors & <a href="http://www.thunderforest.com/">Thunderforest</a>'
    }
  },
  components: {
    // BrowserPrint,
    DeathMarker,
    LMap,
    LTileLayer
  },
  mounted() {
    let url = 'https://raw.githubusercontent.com/pvanheus/1976/master/1976_cape_deaths.json';
    axios.get(url).then(response => {
      this.deaths = response.data;
      this.$nextTick( () => {
        if (this.deaths) {
          this.map = this.$refs.map.mapObject;
          this.printButton = L.easyPrint({
            sizeModes: [{
              width: 5961,
              height: 5961,
              name: 'A0 Portrait',
              className: 'a0CssClass',
              tooltip: 'Custom A0 Size (300dpi)'
            }, 'A4Portrait']
          }).addTo(this.map);
        }
      });
    });
  }
}
</script>

<style scoped>
#map {
  width: 1024px;
  height: 1024px;
}
  .easyPrintHolder .a0CssClass {
    background-image: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIgogICB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgd2lkdGg9IjU5NG1tIgogICB2ZXJzaW9uPSIxLjEiCiAgIGhlaWdodD0iODQxbW0iCiAgIHZpZXdCb3g9IjAgMCA4OTgwLjE1NyAxMjcxNC4zMzEiCiAgIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXcgMCAwIDY0IDY0IgogICBpZD0ic3ZnODU1IgogICBzb2RpcG9kaTpkb2NuYW1lPSJiNjQuc3ZnIgogICBpbmtzY2FwZTp2ZXJzaW9uPSIwLjkyLjMgKDI0MDU1NDYsIDIwMTgtMDMtMTEpIj4KICA8bWV0YWRhdGEKICAgICBpZD0ibWV0YWRhdGE4NjEiPgogICAgPHJkZjpSREY+CiAgICAgIDxjYzpXb3JrCiAgICAgICAgIHJkZjphYm91dD0iIj4KICAgICAgICA8ZGM6Zm9ybWF0PmltYWdlL3N2Zyt4bWw8L2RjOmZvcm1hdD4KICAgICAgICA8ZGM6dHlwZQogICAgICAgICAgIHJkZjpyZXNvdXJjZT0iaHR0cDovL3B1cmwub3JnL2RjL2RjbWl0eXBlL1N0aWxsSW1hZ2UiIC8+CiAgICAgICAgPGRjOnRpdGxlPjwvZGM6dGl0bGU+CiAgICAgIDwvY2M6V29yaz4KICAgIDwvcmRmOlJERj4KICA8L21ldGFkYXRhPgogIDxkZWZzCiAgICAgaWQ9ImRlZnM4NTkiIC8+CiAgPHNvZGlwb2RpOm5hbWVkdmlldwogICAgIHBhZ2Vjb2xvcj0iI2ZmZmZmZiIKICAgICBib3JkZXJjb2xvcj0iIzY2NjY2NiIKICAgICBib3JkZXJvcGFjaXR5PSIxIgogICAgIG9iamVjdHRvbGVyYW5jZT0iMTAiCiAgICAgZ3JpZHRvbGVyYW5jZT0iMTAiCiAgICAgZ3VpZGV0b2xlcmFuY2U9IjEwIgogICAgIGlua3NjYXBlOnBhZ2VvcGFjaXR5PSIwIgogICAgIGlua3NjYXBlOnBhZ2VzaGFkb3c9IjIiCiAgICAgaW5rc2NhcGU6d2luZG93LXdpZHRoPSIyODgwIgogICAgIGlua3NjYXBlOndpbmRvdy1oZWlnaHQ9IjE0OTEiCiAgICAgaWQ9Im5hbWVkdmlldzg1NyIKICAgICBzaG93Z3JpZD0iZmFsc2UiCiAgICAgdW5pdHM9Im1tIgogICAgIGlua3NjYXBlOnpvb209IjAuMjExODIxMyIKICAgICBpbmtzY2FwZTpjeD0iMzAwMy42MjQzIgogICAgIGlua3NjYXBlOmN5PSIxODU5Ljc1MDMiCiAgICAgaW5rc2NhcGU6d2luZG93LXg9IjAiCiAgICAgaW5rc2NhcGU6d2luZG93LXk9IjU1IgogICAgIGlua3NjYXBlOndpbmRvdy1tYXhpbWl6ZWQ9IjEiCiAgICAgaW5rc2NhcGU6Y3VycmVudC1sYXllcj0ic3ZnODU1Ij4KICAgIDxzb2RpcG9kaTpndWlkZQogICAgICAgcG9zaXRpb249IjAsMCIKICAgICAgIG9yaWVudGF0aW9uPSIwLDIyNDUuMDM5NCIKICAgICAgIGlkPSJndWlkZTg2MyIKICAgICAgIGlua3NjYXBlOmxvY2tlZD0iZmFsc2UiIC8+CiAgICA8c29kaXBvZGk6Z3VpZGUKICAgICAgIHBvc2l0aW9uPSI4OTgwLjE1NzMsMCIKICAgICAgIG9yaWVudGF0aW9uPSItMzE3OC41ODI3LDAiCiAgICAgICBpZD0iZ3VpZGU4NjUiCiAgICAgICBpbmtzY2FwZTpsb2NrZWQ9ImZhbHNlIiAvPgogICAgPHNvZGlwb2RpOmd1aWRlCiAgICAgICBwb3NpdGlvbj0iODk4MC4xNTczLDEyNzE0LjMzMSIKICAgICAgIG9yaWVudGF0aW9uPSIwLC0yMjQ1LjAzOTQiCiAgICAgICBpZD0iZ3VpZGU4NjciCiAgICAgICBpbmtzY2FwZTpsb2NrZWQ9ImZhbHNlIiAvPgogICAgPHNvZGlwb2RpOmd1aWRlCiAgICAgICBwb3NpdGlvbj0iMCwxMjcxNC4zMzEiCiAgICAgICBvcmllbnRhdGlvbj0iMzE3OC41ODI3LDAiCiAgICAgICBpZD0iZ3VpZGU4NjkiCiAgICAgICBpbmtzY2FwZTpsb2NrZWQ9ImZhbHNlIiAvPgogIDwvc29kaXBvZGk6bmFtZWR2aWV3PgogIDxwYXRoCiAgICAgZD0iTSAzNTUyLjI1NzQsODc2Mi42MDc4IDU2NC44NzI5MywxMTc1MC4xMzMgdiAtMTQ4NC42MiBjIDAsLTE1NS44NDYgLTEyNi4xNjgwOCwtMjgyLjQzNjUgLTI4Mi40MzY0NywtMjgyLjQzNjUgQyAxMjYuMzA4NzQsOTk4My4wNzY1IDAsMTAxMDkuNTI2IDAsMTAyNjUuNTEzIHYgMjE2Ni4zNzggYyAwLDM2LjcxMSA3LjQ1NDc0NzMsNzMuMjgxIDIxLjgwMTYyLDEwNy44ODMgMjguNTUzMDg4LDY5LjIwMiA4My41NDk0MywxMjQuMDU4IDE1Mi43NTE5OSwxNTIuODkyIDM0LjQ2MDYzLDE0LjIwNiA3MS4xNzE3NCwyMS42NjEgMTA3Ljg4Mjg1LDIxLjY2MSBIIDI0NDguOTU0OCBjIDE1NS45ODcxLDAgMjgyLjQzNjUsLTEyNi4zMDkgMjgyLjQzNjUsLTI4Mi40MzYgMCwtMTU2LjEyOCAtMTI2LjMwODcsLTI4Mi40MzcgLTI4Mi40MzY1LC0yODIuNDM3IEggOTY0LjE5NDIxIEwgMzk1MS40MzgxLDkxNjEuOTI5MSBjIDExMC4yNzM5LC0xMTAuMjc0IDExMC4yNzM5LC0yODkuMDQ3MyAwLC0zOTkuMzIxMyAtMTEwLjI3NCwtMTEwLjI3NCAtMjg4LjkwNjcsLTExMC4yNzQgLTM5OS4xODA3LDAgeiIKICAgICBpZD0icGF0aDg0NyIKICAgICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICAgIHN0eWxlPSJmaWxsOiMwMDAwMDA7c3Ryb2tlLXdpZHRoOjE0MC42NTU2MDkxMyIgLz4KICA8cGF0aAogICAgIGQ9Im0gODk4MC4xNTczLDE5Ni41NzI0NCBjIC0yOC41NTMxLC02OS4wNjE5IC04My41NDk0LC0xMjQuMDU4MTk4IC0xNTIuNzUyLC0xNTIuODkyNTk4IC0zNC40NjA2LC0xNC4yMDYzIC03MS4xNzE3LC0yMS42NjEgLTEwNy44ODI4LC0yMS42NjEgSCA2NTUzLjAwNDEgYyAtMTU1Ljk4NzEsMCAtMjgyLjQzNjUsMTI2LjMwODY5OCAtMjgyLjQzNjUsMjgyLjQzNjQ5OCAwLDE1Ni4xMjc3IDEyNi4zMDg4LDI4Mi40MzY0IDI4Mi40MzY1LDI4Mi40MzY0IEggODAzNy43NjQ3IEwgNTA1MC41MjA5LDM1NzQuNDE2OSBjIC0xMTAuMjc0LDExMC4yNzQgLTExMC4yNzQsMjg5LjA0NzMgMCwzOTkuMzIxMyA1NS4xMzcsNTUuMTM3IDEyNy40MzQsODIuODQ2MSAxOTkuNzMxLDgyLjg0NjEgNzIuMjk2OSwwIDE0NC40NTMzLC0yNy43MDkxIDE5OS41OTAzLC04Mi44NDYxIEwgODQzNy4wODYsOTg2LjIxMzA0IFYgMjQ3MC44MzMgYyAwLDE1NS44NDY0IDEyNi4xNjgxLDI4Mi40MzY0IDI4Mi40MzY1LDI4Mi40MzY0IDE1NS45ODcsMCAyODIuNDM2NCwtMTI2LjQ0OTQgMjgyLjQzNjQsLTI4Mi40MzY0IFYgMzA0LjQ1NTM0IGMgMCwtMzYuNzExMSAtNy40NTQ3LC03My40MjIzIC0yMS44MDE2LC0xMDcuODgyOSB6IgogICAgIGlkPSJwYXRoODQ5IgogICAgIGlua3NjYXBlOmNvbm5lY3Rvci1jdXJ2YXR1cmU9IjAiCiAgICAgc3R5bGU9ImZpbGw6IzAwMDAwMDtzdHJva2Utd2lkdGg6MTQwLjY1NTYwOTEzIiAvPgo8L3N2Zz4K=);
  }
</style>
