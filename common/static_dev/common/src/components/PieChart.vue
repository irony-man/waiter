<template>
  <div class="w-100">
    <apexchart
      :series="series"
      :options="options"
      type="pie"/>
  </div>
</template>

<script>
export default {
  name: "PieChart",
  props: {
    series: {
      type: Array,
      required: true,
    },
    labels: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      options: {
        labels: this.labels,
      },
    };
  },
};
</script>
