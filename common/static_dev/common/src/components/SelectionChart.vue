<template>
  <div>
    <SegmentTitle text="Selection"/>
    <apexchart
      type="bar"
      :options="options"
      :series="[{name: 'Percentage', data: percent}]"/>
  </div>
</template>

<script>
import SegmentTitle from "./SegmentTitle.vue";
import {themeColorArray} from "../mathLib.js";

export default {
  name: "SelectionChart",
  components: {SegmentTitle},
  props: {
    percent: {
      type: Array,
      required: true,
    },
    categories: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      options: {
        colors: [themeColorArray()[0]],
        markers: {
          size: 0,
        },
        chart: {
          toolbar: {
            show: false,
          },
        },
        dataLabels: {
          enabled: true,
          formatter: function (val) {
            return (val * 100).toFixed(2) + "%";
          },
        },
        yaxis: {
          title: {
            text: '% Allocated'
          },
          labels: {
            formatter: function (val) {
              return (val * 100).toFixed(0);
            },
          },
        },
        xaxis: {
          categories: this.categories,
        }
      },
    };
  }
};
</script>
