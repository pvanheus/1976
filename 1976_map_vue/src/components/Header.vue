<template>
  <div class="container">
    <div class="row">
      <div class="col s8 offset-s2">
        <div id="header">
          <h4>In memory of 1976</h4>
          <p>
            June 16 1976 marks the start of the 1976 youth uprising against
            Apartheid in South Africa. Most closely associated with the school
            students march in Soweto and the murder of Hector Pieterson, the
            revolt spread across the country and well past June 1976. Along with
            the revolt came the deaths, most often of those shot by police. The
            South African History Online website has tried to collect a
            <a
              href="http://www.sahistory.org.za/topic/june-16-soweto-youth-uprising"
              >list</a
            >
            of the "casaulties of 1976". I have taken that list, done a little
            cleanup (code is
            <a href="https://github.com/pvanheus/1976">here</a>) and produced
            the map below.
          </p>
        </div>
        <div id="map" class="map"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style scoped></style>
