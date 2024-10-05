<template>
  <div class="table-responsive">
    <table class="table">
      <caption class="ms-auto">
        <slot name="content"/>
      </caption>
      <thead>
        <tr>
          <th
            v-for="col in columns"
            :key="col"
            :class="{ 'text-end': rightAligned.indexOf(col) > -1 }">
            {{ col }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="row in getData()"
          :key="row[rowKey]">
          <td
            v-for="col in columns"
            :key="col"
            :class="{'text-end': rightAligned.indexOf(col) > -1}">
            <router-link
              v-if="linkGetter(col, row)"
              :to="linkGetter(col, row)">
              {{ formattedValue(col, row[col]) }}
            </router-link>
            <span v-else>
              {{ formattedValue(col, row[col]) }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import objectLib from "../objectLib.js";

export default {
  name: "DataTable",
  props: {
    dataList: {
      type: Array,
      required: true,
    },
    columns: {
      type: Array,
      required: true,
    },
    rightAligned: {
      type: Array,
      required: true,
    },
    currencyTypes: {
      type: Array,
      required: true,
    },
    percentTypes: {
      type: Array,
      required: true,
    },
    rowKey: {
      type: String,
      required: true,
    },
    mapping: {
      type: Array,
      required: false,
      default: () => null,
    },
    linkGetter: {
      type: Function,
      required: false,
      default: () => null
    },
  },
  methods: {
    getData() {
      if (this.mapping) {
        return this.dataList.map(row => {
          const data = {};
          this.mapping.forEach(map => {
            if (map.display) {
              data[map.target] = objectLib.recursiveGet(row, map.source);
            }
          });
          return { [this.rowKey]: row[this.rowKey], ...data };
        });
      }

      return this.dataList;
    },
    formattedValue(col, value) {
      if (Number.isFinite(value)) {
        if (this.currencyTypes.indexOf(col) > -1) {
          return this.$filters.formatCurrency(value);
        } else if (this.percentTypes.indexOf(col) > -1) {
          return this.$filters.formatPercentage(value);
        }
        return this.$filters.formatNumber(value);
      }
      return value;
    },
  },
};
</script>
