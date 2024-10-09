<template>
  <Loader ref="loader">
    <div class="container my-5">
      <Empty
        v-if="!!instance.notFound"
        title="Restaurant not Found"
        text="The restaurant you are looking for is not in this chain."
        icon="fas fa-face-frown"/>
      <div v-else>
        <PageTitle
          class="border-bottom pb-4"
          :secondary="`<div class='fs-6 mb-2'>Restaurant: <strong>${table.restaurant.name}</strong></div>`"
          :primary="`Ordering from Table: <strong>#${table.number}</strong>`"/>

        <div class="mt-5">
          <h6 class="fw-bold mb-3 text-uppercase">
            Categories
          </h6>

          <Empty
            v-if="!categories.length"
            title="No Categories"
            text="You don't have any categories for this restaurant."
            icon="fas fa-face-frown"/>

          <div v-else>
            <div class="row justify-content-center g-5">
              <div
                v-for="category in categories"
                :key="category.uid"
                class="col-6 col-md-4 col-lg-3 col-xl-2">
                <router-link
                  :to="{ name: 'table-category', params: { categoryUid: category.uid, tableUid: tableUid, } }">
                  <div class="card bg-secondary text-center h-100">
                    <div class="icon-img-container">
                      <img
                        v-if="category.image"
                        :src="category.image"
                        :alt="category.name">
                      <img
                        v-else
                        src="@/assets/images/plate.png"
                        :alt="category.name">
                    </div>
                    <div class="card-body">
                      <div class="card-text fw-normal">
                        {{ category.name }}
                      </div>
                    </div>
                  </div>
                </router-link>
              </div>
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

export default {
  name: "TableView",
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, CategoryFormModal },
  data() {
    return {
      table: {},
      instance: {},
      showModal: false,
      deleting: false,
      deletingTable: false,
      tableCreating: false,
      categories: {
        results: [],
        page: 0,
        loading: false,
      },
    };
  },
  computed: {
    ...mapState(["user"]),
    tableUid() {
      return this.$route.params.uid;
    },
    limit() {
      return 30;
    },
    routerItems() {
      return [{
        name: this.user.chain_name,
        to: { name: 'dashboard' }
      }];
    }
  },
  async mounted() {
    try {
      const response = await this.getTableQRCode({uid: this.tableUid});
      this.categories = response.categories;
      this.table = response.table;
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
