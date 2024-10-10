<template>
  <div
    id="menu-item-form"
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
              class="modal-title fs-5">
              Menu Item Form
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
              <Switch
                v-model="instance.has_half_price"
                label="Has Half Price"
                name="has_half_price"
                :error="errors.has_half_price"
                @input="onHasHalfPrichChange"/>
            </div>
            <div
              v-if="instance.has_half_price"
              class="mb-3">
              <Input
                v-model="instance.half_price"
                type="number"
                label="Half Price"
                name="half_price"
                addon="<i class='fas fa-indian-rupee-sign'></i>"
                :min="0"
                required
                :error="errors.half_price"/>
            </div>
            <div class="mb-3">
              <Input
                v-model="instance.full_price"
                type="number"
                :label="instance.has_half_price ? 'Full Price': 'Price'"
                name="full_price"
                addon="<i class='fas fa-indian-rupee-sign'></i>"
                :min="0"
                required
                :error="errors.full_price"/>
            </div>
            <div class="mb-3">
              <Select
                v-model="instance.menu_type"
                label="Type"
                name="menu_type"
                :source="{ array: user.choices.menu_type }"
                required
                :error="errors.menu_type"/>
            </div>
            <div class="mb-3">
              <Select
                v-model="instance.category"
                label="Category"
                name="category"
                track-by="uid"
                :source="{ fetchFunction: listCategory }"
                required
                :disabled="!!menuItem.category"
                :error="errors.category"/>
            </div>
            <div class="mb-3">
              <Switch
                v-model="instance.available"
                label="Available"
                name="available"
                :error="errors.available"/>
            </div>
            <div class="mb-3">
              <TextArea
                v-model="instance.description"
                label="Description"
                name="description"
                :error="errors.description"/>
            </div>
          </div>
          <div class="modal-footer justify-content-start">
            <LoadingButton
              :is-loading="!!instance.submitting"
              class="btn-primary"
              btn-type="submit">
              Save Menu Item
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
import Switch from "./Switch.vue";

export default {
  name: "MenuItemFormModal",
  components: { Input, TextArea, Button, LoadingButton, Select, Loader, Switch },
  props: {
    menuItem: {
      type: Object,
      required: false,
      default: () => { }
    },
  },
  emits: ['closed', 'saved',],
  data() {
    return { modalEl: null, instance: { menu_type: 'VEG', available: true }, errors: {} };
  },
  computed: {
    ...mapState(["user"]),
  },
  mounted() {
    this.instance = { ...this.instance, ...this.menuItem };
    this.instance.has_half_price = parseFloat(this.instance.half_price) != 0;
    this.$refs.loader.complete();
    this.modalEl = document.getElementById('menu-item-form');
    this.modal = new window.bootstrap.Modal(this.modalEl, { backdrop: 'static', keyboard: true });
    this.modalEl.addEventListener('hidden.bs.modal', () => this.$emit('closed'));
    if (this.modal) {
      this.modal.show();
    }
  },
  beforeUnmount() {
    if (this.modal) {
      this.modal.hide();
    }
  },
  methods: {
    ...mapActions(['listCategory', 'createMenuItem', 'updateMenuItem']),
    async submitItem() {
      try {
        this.instance.submitting = true;
        this.instance.menu_type = this.instance.menu_type?.value ?? this.instance.menu_type;
        if (this.instance.uid) {
          this.instance = await this.updateMenuItem({ uid: this.instance.uid, formData: this.instance });
        } else {
          this.instance = await this.createMenuItem(this.instance);
        }
        this.$toast.success("Item saved!!");
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
    },
    onHasHalfPrichChange(e) {
      const value = e.target.value;
      console.log(value);
      if (!value) {
        this.instance.half_price = 0;
      }
    }
  }
};
</script>
