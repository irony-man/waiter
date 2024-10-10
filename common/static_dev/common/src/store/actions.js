import {getRequest, getUrl, deleteRequest } from "./network";
import Types from "./types.js";
import GeneratedActions from './actions.gen.js';

export default {
  async getUser({ commit }) {
    const url = getUrl("user/me");
    const response = await getRequest(url);
    commit(Types.SET_USER, response);
    return response;
  },

  async getCart({ commit }) {
    const cart = localStorage.getItem('cart') || '{}';
    const response = await getRequest('/get-cart/', {cart});
    commit(Types.SET_CART, response);
    return response;
  },

  async getLocalCart({ commit }) {
    const cart = await JSON.parse(localStorage.getItem('cart')) || {};
    commit(Types.SET_CART, cart);
    return cart;
  },

  setCart({ commit }, cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  async deleteRestaurantTable(ctx, uid) {
    const url = getUrl(`restaurant/${uid}/table`);
    return await deleteRequest(url);
  },

  async getTableQRCode(ctx, {uid, query}) {
    const url = `/table-qr-code/${uid}/`;
    return await getRequest(url, query);
  },

  ...GeneratedActions,
};
