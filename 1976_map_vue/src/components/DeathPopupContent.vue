<template>
  <div>
    <span><b>{{ this.personWithAge }}</b></span><br />
    <span class="deathdate">{{ this.deathDate }}</span><br />
    <span class="location">{{ this.death.location }}</span><br />
    <span class="deathdetail">{{ this.death.detail }}</span><br />
  </div>
</template>

<script>
export default {
  name: 'DeathPopupContent',
  props: {
    death: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      personWithAge: `${this.death.person} ${this.death.age}`
    }
  },
  computed: {
    deathDate() {
      let date = new Date(this.death.timestamp * 1000)

      return `${date.getDay()} ${date.getMonth()} ${date.getFullYear()}`
    }
  }
}
</script>

<style scoped></style>
