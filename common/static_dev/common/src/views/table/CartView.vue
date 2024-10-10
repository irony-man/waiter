<template>
  <Loader ref="loader">
    <div>
      <Breadcrumb
        :router-items="routerItems"
        name="Cart"/>
      <PageTitle
        class="border-bottom pb-4"
        :secondary="`<div class='fs-6 mb-2'>Restaurant: <strong>${instance.table.restaurant?.name}</strong></div>`"
        :primary="`Ordering from Table: <strong>#${instance.table.number}</strong>`"/>

      <div class="mt-5">
        <h6 class="fw-bold mb-3 text-uppercase">
          Cart
        </h6>
      </div>
    </div>
  </Loader>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Loader from "@/components/Loader.vue";
import PageTitle from "@/components/PageTitle.vue";
import Empty from "@/components/Empty.vue";
import Breadcrumb from "@/components/Breadcrumb.vue";
import LoadingButton from "@/components/LoadingButton.vue";
import Button from "@/components/Button.vue";
import CategoryFormModal from "@/components/CategoryFormModal.vue";
import { HttpNotFound, HttpServerError } from "@/store/network";
import CategoryCard from "@/components/CategoryCard.vue";

export default {
  name: "CartView",
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, CategoryFormModal, CategoryCard },
  data() {
    return {
      instance: {
        cart: {},
        table: {}
      },
    };
  },
  computed: {
    ...mapState(["cart"]),
    tableUid() {
      return this.$route.params.tableUid;
    },
    routerItems() {
      return [{
        name: this.instance.table.restaurant?.name,
        to: { name: 'table', params: { uid: this.tableUid } }
      }];
    }
  },
  async mounted() {
    try {
      this.instance = await this.getTableQRCode({ uid: this.tableUid });
    } catch (error) {
      console.error(error);
      let message = "Error fetching Table!!";
      if (error instanceof HttpNotFound) {
        this.instance.notFound = true;
        message = error.data?.detail ?? "Table not found!!";
      } else if (error instanceof HttpServerError) {
        message = this.error.message;
      }
      this.$toast.error(message);
    } finally {
      this.$refs.loader.complete();
    }
  },
  methods: {
    ...mapActions(['getTableQRCode',]),
  }
};
</script>
