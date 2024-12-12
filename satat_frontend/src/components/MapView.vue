<template>
<div style="height: 100%; width: 100%">
    <l-map
      v-if="showMap"
      :zoom="zoom"
      :center="center"
      :options="mapOptions"

      style="height: 100%"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-marker :lat-lng="groundstation"/>
      <l-marker :lat-lng="satellite"/>

    </l-map>
  </div>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue3-leaflet";
import axios from 'axios';

export default {
  name: "MapView",
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  beforeCreate(){
    axios
        .get('/track/satellite/1/positions')
        .then(response => {
            const gs = response.data.ground_station;
            const sat = response.data.satellite;
            this.groundstation = latLng(gs.lat, gs.long);
            this.center = latLng(gs.lat, gs.long);
            this.currentCenter = latLng(gs.lat, gs.long);
            this.satellite = latLng(sat.lat, sat.long)
        })
        .catch(error => {
            console.log(error);
        })
  },
  data() {
    return {
      zoom: 3,
      center: latLng(0,0),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      groundstation: latLng(0, 0),
      satellite: latLng(0.0, 0.0),
      currentZoom: 3,
      currentCenter: latLng(0,0),
      mapOptions: {
        zoomSnap: 0.5
      },
      showMap: true
    };
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    innerClick() {
      alert("Click!");
    }
  }
};
</script>