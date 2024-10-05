<template>
  <div
    id="category-form"
    class="modal fade"
    tabindex="-1">
    <div class="modal-dialog">
      <Loader ref="loader">
        <form
          method="post"
          class="modal-content"
          @submit.prevent="submitItem">
          <div class="modal-header">
            <h1
              id="exampleModalLabel"
              class="modal-title fs-5">
              Category Form
            </h1>
            <Button
              class="btn-close"
              data-bs-dismiss="modal"/>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <Input
                v-model="instance.name"
                label="Name"
                name="name"
                required
                :error="errors.name"/>
            </div>
            <div class="mb-3">
              <Select
                v-model="instance.restaurant"
                label="Restaurant"
                name="restaurant"
                track-by="uid"
                :source="{ fetchFunction: listRestaurant }"
                required
                :disabled="!!category.restaurant"
                :error="errors.restaurant"/>
            </div>
          </div>
          <div class="modal-footer justify-content-start">
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-primary"
              btn-type="submit">
              Save Category
            </LoadingButton>
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-secondary"
              data-bs-dismiss="modal">
              Close
            </LoadingButton>
          </div>
        </form>
      </Loader>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import Button from './Button.vue';
import LoadingButton from './LoadingButton.vue';
import Input from './Input.vue';
import TextArea from './TextArea.vue';
import Select from './Select.vue';
import Loader from './Loader.vue';
import { HttpBadRequestError } from "../store/network";

export default {
  name: "CategoryFormModal",
  components: { Input, TextArea, Button, LoadingButton, Select, Loader },
  props: {
    category: {
      type: Object,
      required: false,
      default: () => { }
    },
  },
  emits: ['closed', 'saved',],
  data() {
    return { modalEl: null, instance: { menu_type: 'VEG' }, errors: {} };
  },
  computed: {
    ...mapState(["user"]),
  },
  mounted() {
    this.$refs.loader.complete();
    this.modalEl = document.getElementById('category-form');
    this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
    this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
    if (this.modal) {
      this.modal.show();
    }
    this.instance = { ...this.instance, ...this.category };
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
  methods: {
    ...mapActions(['listRestaurant', 'createCategory', 'updateCategory']),
    async submitItem() {
      try {
        this.instance.submitting = true;
        if (this.instance.uid) {
          this.instance = await this.updateCategory({ uid: this.instance.uid, formData: this.instance });
        } else {
          this.instance = await this.createCategory(this.instance);
        }
        this.$emit('saved', this.instance);
      } catch (error) {
        if (error instanceof HttpBadRequestError) {
          this.errors = error.data;
        }
        this.$toast.error("Error saving Item!!");
        console.error(error);
      } finally {
        this.instance.submitting = false;
      }
    }
  }
};
</script>
