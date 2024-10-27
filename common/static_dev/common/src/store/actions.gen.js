
import {
  getRequest,
  getUrl,
  postRequest,
  patchRequest,
  deleteRequest
} from "./network";

export default {

  async listCategory(ctx, query) {
    const url = getUrl("category");
    return await getRequest(url, query);
  },

  async getCategory(ctx, uid) {
    const url = getUrl(`category/${uid}`);
    return await getRequest(url);
  },

  async createCategory(ctx, formData) {
    const url = getUrl("category");
    return await postRequest(url, formData);
  },

  async updateCategory(ctx, {uid, formData}) {
    const url = getUrl(`category/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdateCategory(ctx, {uid, formData}) {
    return await uid?this.updateCategory(ctx, {uid, formData}):this.createCategory(ctx, formData);
  },

  async deleteCategory(ctx, uid) {
    const url = getUrl(`category/${uid}`);
    return await deleteRequest(url);
  },


  async listChain(ctx, query) {
    const url = getUrl("chain");
    return await getRequest(url, query);
  },

  async getChain(ctx, uid) {
    const url = getUrl(`chain/${uid}`);
    return await getRequest(url);
  },

  async createChain(ctx, formData) {
    const url = getUrl("chain");
    return await postRequest(url, formData);
  },

  async updateChain(ctx, {uid, formData}) {
    const url = getUrl(`chain/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdateChain(ctx, {uid, formData}) {
    return await uid?this.updateChain(ctx, {uid, formData}):this.createChain(ctx, formData);
  },

  async deleteChain(ctx, uid) {
    const url = getUrl(`chain/${uid}`);
    return await deleteRequest(url);
  },


  async listMenuItem(ctx, query) {
    const url = getUrl("menu-item");
    return await getRequest(url, query);
  },

  async getMenuItem(ctx, uid) {
    const url = getUrl(`menu-item/${uid}`);
    return await getRequest(url);
  },

  async createMenuItem(ctx, formData) {
    const url = getUrl("menu-item");
    return await postRequest(url, formData);
  },

  async updateMenuItem(ctx, {uid, formData}) {
    const url = getUrl(`menu-item/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdateMenuItem(ctx, {uid, formData}) {
    return await uid?this.updateMenuItem(ctx, {uid, formData}):this.createMenuItem(ctx, formData);
  },

  async deleteMenuItem(ctx, uid) {
    const url = getUrl(`menu-item/${uid}`);
    return await deleteRequest(url);
  },


  async listOrder(ctx, query) {
    const url = getUrl("order");
    return await getRequest(url, query);
  },

  async getOrder(ctx, uid) {
    const url = getUrl(`order/${uid}`);
    return await getRequest(url);
  },

  async createOrder(ctx, formData) {
    const url = getUrl("order");
    return await postRequest(url, formData);
  },

  async updateOrder(ctx, {uid, formData}) {
    const url = getUrl(`order/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdateOrder(ctx, {uid, formData}) {
    return await uid?this.updateOrder(ctx, {uid, formData}):this.createOrder(ctx, formData);
  },

  async deleteOrder(ctx, uid) {
    const url = getUrl(`order/${uid}`);
    return await deleteRequest(url);
  },


  async listRestaurant(ctx, query) {
    const url = getUrl("restaurant");
    return await getRequest(url, query);
  },

  async getRestaurant(ctx, uid) {
    const url = getUrl(`restaurant/${uid}`);
    return await getRequest(url);
  },

  async createRestaurant(ctx, formData) {
    const url = getUrl("restaurant");
    return await postRequest(url, formData);
  },

  async updateRestaurant(ctx, {uid, formData}) {
    const url = getUrl(`restaurant/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdateRestaurant(ctx, {uid, formData}) {
    return await uid?this.updateRestaurant(ctx, {uid, formData}):this.createRestaurant(ctx, formData);
  },

  async deleteRestaurant(ctx, uid) {
    const url = getUrl(`restaurant/${uid}`);
    return await deleteRequest(url);
  },


  async listTable(ctx, query) {
    const url = getUrl("table");
    return await getRequest(url, query);
  },

  async getTable(ctx, uid) {
    const url = getUrl(`table/${uid}`);
    return await getRequest(url);
  },

  async createTable(ctx, formData) {
    const url = getUrl("table");
    return await postRequest(url, formData);
  },

  async updateTable(ctx, {uid, formData}) {
    const url = getUrl(`table/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdateTable(ctx, {uid, formData}) {
    return await uid?this.updateTable(ctx, {uid, formData}):this.createTable(ctx, formData);
  },

  async deleteTable(ctx, uid) {
    const url = getUrl(`table/${uid}`);
    return await deleteRequest(url);
  },

};
