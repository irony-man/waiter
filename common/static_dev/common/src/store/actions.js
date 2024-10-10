import { getRequest, getUrl, deleteRequest } from "./network";
import Types from "./types.js";
import GeneratedActions from "./actions.gen.js";

export default {
  async getUser({ commit }) {
    const url = getUrl("user/me");
    const response = await getRequest(url);
    commit(Types.SET_USER, response);
    return response;
  },

  addCartItem({ commit, state }, item) {
    const { cart } = state;
    const {price_type} = item;
    const price = price_type === "FULL" ? item.full_price : item.half_price;
    const key = `${item.uid}/${price_type}`;
    let quantity = (key in cart ? cart[key].quantity : 0) + 1;
    cart[key] = { price, quantity, price_type, menu_item: item };

    localStorage.setItem("cart", JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  removeCartItem({ commit, state }, {item, priceTypes= ['HALF', 'FULL']}) {
    const { cart } = state;
    for (const type of priceTypes) {
      const key = `${item.uid}/${type}`;
      if (key in cart) {
        const quantity = Math.max(--cart[key].quantity, 0);
        if(quantity === 0) {
          delete cart[key];
        }
        break;
      }
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  setCart({ commit }, cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
    commit(Types.SET_CART, cart);
  },

  async deleteRestaurantTable(ctx, uid) {
    const url = getUrl(`restaurant/${uid}/table`);
    return await deleteRequest(url);
  },

  async getTableQRCode(ctx, { uid, query }) {
    const url = `/table-qr-code/${uid}/`;
    return await getRequest(url, query);
  },

  async getCart(ctx, uid) {
    const response = await getRequest(`/table-qr-code/${uid}/`, {
      cart: localStorage.getItem("cart") || "{}",
    });
    ctx.commit(Types.SET_CART, response.cart);
    return response;
  },

  ...GeneratedActions,
};
