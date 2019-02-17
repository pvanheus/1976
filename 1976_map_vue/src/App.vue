<template>
  <div class="row">
    <div class="col s8 offset-s2">
      <Header />
      <Map />
    </div>
  </div>
</template>

<script>
import Header from "./components/Header";
import Map from "./components/Map";

export default {
  name: 'MainPage',
  components: {
    Header,
    Map
  }
};
</script>

<style></style>
