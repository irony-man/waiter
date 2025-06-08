<template>
  <Loader ref="loader">
    <div
      class="container my-5">
      <Empty
        v-if="!!restaurant.notFound"
        title="Restaurant not Found"
        text="The restaurant you are looking for is not in this chain."
        icon="fas fa-face-frown"/>
      <div
        v-else>
        <Breadcrumb
          :router-items="routerItems"
          :name="restaurant.name"/>
        <PageTitle
          class="border-bottom pb-4"
          :secondary="`A restaurant of <strong class='text-primary'>${user.chain_name}</strong>.`"
          :primary="restaurant.name">
          <template #right>
            <LoadingButton
              class="btn-outline-danger"
              :is-loading="!!deleting"
              btn-icon="fas fa-trash me-2"
              @click="removeRestaurant">
              Delete Restaurant
            </LoadingButton>
          </template>
        </PageTitle>


        <div class="mb-5">
          <div class="d-flex gap-3 flex-wrap align-items-center mb-4 g-4">
            <div class="flex-grow-1">
              <h6 class="fw-bold mb-0 text-uppercase">
                Tables
              </h6>
            </div>

            <div class="d-flex gap-3 flex-wrap align-items-center">
              <LoadingButton
                :is-loading="tableCreating"
                class="btn-primary"
                btn-icon="fas fa-plus me-2"
                @click="saveTable">
                Add Table
              </LoadingButton>
              <LoadingButton
                v-if="tableData.results.length"
                class="btn-outline-danger"
                :is-loading="!!deletingTable"
                btn-icon="fas fa-trash me-2"
                @click="removeTable">
                Delete Table
              </LoadingButton>
            </div>
          </div>
          <Empty
            v-if="!tableData.results.length"
            title="No Tables"
            text="You don't have any tables in this restaurant."
            icon="fas fa-face-frown"/>

          <div
            v-else
            class="row g-5">
            <div
              v-for="table in tableData.results"
              :key="table.uid"
              class="col-12 col-sm-6 col-md-4">
              <div class="card border-3 border-primary-subtle h-100">
                <div class="card-header">
                  Table number <span class="fw-bold">#{{ table.number }}</span>
                </div>
                <img
                  class="img card-img-bottom"
                  :src="table.qr_code_url"
                  :alt="`Table number ${table.number}`">
              </div>
            </div>
            <div
              v-if="tableData.next"
              class="mt-5 text-center">
              <LoadingButton
                :is-loading="!!tableData.loading"
                class="btn-primary"
                btn-type="button"
                @click="fetchTable()">
                Load More
              </LoadingButton>
            </div>
          </div>
        </div>

        <div class="mb-5">
          <div class="d-flex gap-3 flex-wrap align-items-center mb-4 g-4">
            <div class="flex-grow-1">
              <h6 class="fw-bold mb-0 text-uppercase">
                Categories
              </h6>
            </div>
            <div class="d-flex gap-3 flex-wrap align-items-center">
              <Button
                class="btn-primary"
                btn-icon="fas fa-plus me-2"
                @click="startEditing(-1)">
                Add Category
              </Button>
              <LoadingButton
                v-if="!categoryData.results.length"
                class="btn-warning"
                :is-loading="!!categoryData.importing"
                btn-icon="fas fa-arrow-down me-2"
                @click="importCategory">
                Import Category
              </LoadingButton>
            </div>
          </div>

          <Empty
            v-if="!categoryData.results.length"
            title="No Categories"
            text="You don't have any categories for this restaurant."
            icon="fas fa-face-frown"/>

          <div v-else>
            <div class="row justify-content-center g-5">
              <div
                v-for="category in categoryData.results"
                :key="category.uid"
                class="col-6 col-md-4 col-lg-3 col-xl-2">
                <router-link
                  :to="{ name: 'dashboard-category', params: { uid: category.uid } }">
                  <CategoryCard :category="category"/>
                </router-link>
              </div>
            </div>
            <div
              v-if="categoryData.next"
              class="mt-5 text-center">
              <LoadingButton
                :is-loading="!!categoryData.loading"
                class="btn-primary"
                btn-type="button"
                @click="fetchCategory()">
                Load More
              </LoadingButton>
            </div>
          </div>
        </div>

        <CategoryFormModal
          v-if="showModal"
          :category="instance"
          @closed="showModal = false"
          @saved="saveCategory"/>
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
  name: "RestaurantView",
  components: { PageTitle, Loader, Empty, Button, Breadcrumb, LoadingButton, CategoryFormModal, CategoryCard },
  data() {
    return {
      restaurant: {},
      instance: {},
      showModal: false,
      deleting: false,
      deletingTable: false,
      tableCreating: false,
      tableData: {
        results: [],
        page: 0,
        loading: false,
      },
      categoryData: {
        results: [],
        page: 0,
        loading: false,
        importing: false,
      },
    };
  },
  computed: {
    ...mapState(["user"]),
    restaurantUid() {
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
    await Promise.all([
      this.fetchRestaurant(),
      this.fetchTable(),
      this.fetchCategory(),
    ]);
    this.$refs.loader.complete();
  },
  methods: {
    ...mapActions(['getRestaurant', 'listTable', 'createTable', 'deleteRestaurant', 'deleteRestaurantTable', 'listCategory', 'importRestaurantCategory']),
    async fetchRestaurant() {
      try {
        this.restaurant = await this.getRestaurant(this.restaurantUid);
      } catch (error) {
        console.error(error);
        let message = error?.data?.detail ?? "Error fetching Restaurant!!";
        if(error instanceof HttpNotFound) {
          this.restaurant.notFound = true;
          message = error.data?.detail ?? "Restaurant not found!!";
        } else if(error instanceof HttpServerError) {
          message = this.error.message;
        }
        this.$toast.error(message);
      }
    },
    async fetchCategory() {
      try {
        this.categoryData.loading = true;
        const response = await this.listCategory({ restaurant__uid: this.restaurantUid, limit: this.limit, offset: this.categoryData.page++ * this.limit });
        response.results = [...this.categoryData.results, ...response.results];
        this.categoryData = { ...this.categoryData, ...response };
      } catch (err) {
        this.$toast.error("Error fetching categories!!");
        console.error(err);
      } finally {
        this.categoryData.loading = false;
      }
    },
    async importCategory() {
      try {
        this.categoryData.importing = true;
        await this.importRestaurantCategory(this.restaurantUid);
        await this.saveCategory();
      } catch (err) {
        this.$toast.error("Error fetching categories!!");
        console.error(err);
      } finally {
        this.categoryData.importing = false;
      }
    },
    async fetchTable() {
      try {
        this.tableData.loading = true;
        const response = await this.listTable({ restaurant__uid: this.restaurantUid, limit: this.limit, offset: this.tableData.page++ * this.limit });
        response.results = [...this.tableData.results, ...response.results];
        this.tableData = { ...this.tableData, ...response };
      } catch (err) {
        this.$toast.error("Error fetching tables!!");
        console.error(err);
      } finally {
        this.tableData.loading = false;
      }
    },
    async saveCategory() {
      this.categoryData.results = [];
      this.categoryData.page = 0;
      await this.fetchCategory();
      this.showModal = false;
    },
    startEditing(idx) {
      this.instance = idx === -1 ? {} : this.categoryData.results[idx];
      this.instance.restaurant = this.restaurant;
      this.showModal = true;
    },
    async saveTable() {
      try {
        this.tableCreating = true;
        await this.createTable({restaurant: this.restaurant.uid});
        this.$toast.success("Table created!!");
        this.tableData.results = [];
        this.tableData.page = 0;
        await this.fetchTable();
      } catch (error) {
        this.$toast.error("Error creating table!!");
        console.error(error);
      } finally {
        this.tableCreating = false;
      }
    },
    async removeRestaurant() {
      if(!confirm("Are you sure?")) {
        return;
      }
      try {
        this.deleting = true;
        await this.deleteRestaurant(this.restaurant.uid);
        this.$toast.success("Restaurant deleted!!");
        this.$router.push({ name: 'dashboard' });
      } catch (error) {
        this.$toast.error("Error deleting Restaurant!!");
        console.error(error);
      } finally {
        this.deleting = false;
      }
    },
    async removeTable() {
      if(!confirm("Are you sure?")) {
        return;
      }
      try {
        this.deletingTable = true;
        await this.deleteRestaurantTable(this.restaurant.uid);
        this.$toast.success("Table deleted!!");
        this.tableData.results = [];
        this.tableData.page = 0;
        await this.fetchTable();
      } catch (error) {
        this.$toast.error("Error deleting Table!!");
        console.error(error);
      } finally {
        this.deletingTable = false;
      }
    },
  }
};
</script>
