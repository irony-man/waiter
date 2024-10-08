<template>
  <Loader ref="loader">
    <div>
      <PageTitle
        class="border-bottom pb-4"
        :secondary="`<div class='fs-6 mb-2'>Restaurant: <strong>${instance.table.restaurant?.name}</strong></div>`"
        :primary="`Ordering from Table: <strong>#${instance.table.number}</strong>`"/>

      <div class="mt-5">
        <h6 class="fw-bold mb-3 text-uppercase">
          Categories
        </h6>

        <Empty
          v-if="!instance.categories.length"
          title="No Categories"
          text="You don't have any categories for this restaurant."
          icon="fas fa-face-frown"/>

        <div v-else>
          <div class="row justify-content-center g-5">
            <div
              v-for="category in instance.categories"
              :key="category.uid"
              class="col-6 col-md-4 col-lg-3 col-xl-2">
              <router-link
                :to="{ name: 'table-category', params: { categoryUid: category.uid, tableUid: tableUid, } }">
                <CategoryCard :category="category"/>
              </router-link>
            </div>
          </div>
        </div>
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
  name: "TableView",
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, CategoryFormModal, CategoryCard },
  data() {
    return {
      instance: {
        categories: [],
        table: {}
      },
    };
  },
  computed: {
    ...mapState(["cart"]),
    tableUid() {
      return this.$route.params.tableUid;
    },
  },
  async mounted() {
    try {
      this.instance = await this.getTableQRCode({ uid: this.tableUid, query: {categories: true} });
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
