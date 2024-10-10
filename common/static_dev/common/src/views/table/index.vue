<template>
  <Loader ref="loader">
    <div class="container my-5">
      <Empty
        v-if="notFound"
        title="Restaurant not Found"
        text="The restaurant you are looking for is not in this chain."
        icon="fas fa-face-frown"/>
      <router-view
        v-else
        v-slot="{ Component }">
        <component :is="Component"/>
      </router-view>
    </div>
  </Loader>
</template>

<script>
import Loader from "@/components/Loader.vue";
import Empty from "@/components/Empty.vue";
import { mapActions } from "vuex";
import { HttpNotFound, HttpServerError } from "@/store/network";

export default {
  name: "Table",
  components: { Loader, Empty },
  data() {
    return {
      notFound: false,
    };
  },
  async mounted() {
    try {
      await this.getCart(this.$route.params.tableUid);
    } catch (error) {
      console.error(error);
      let message = error?.data?.detail ?? "Error fetching Table!!";
      if (error instanceof HttpNotFound) {
        this.notFound = true;
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
    ...mapActions(['getCart']),
  },
};
</script>
