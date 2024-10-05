import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "",
    meta: { transitionKey: "home", title: "Home" },
    name: "home",
    component: () => import("../views/Home.vue"),
  }, {
    path: "/restaurant/:uid",
    name: "restaurant",
    meta: {title: "Restaurant"},
    component: () => import("../views/Restaurant.vue"),
  }, {
    path: "/category/:uid",
    name: "category",
    meta: {title: "Category"},
    component: () => import("../views/Category.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/app"),
  scrollBehavior() {
    return { top: 0 };
  },
  routes,
});

router.beforeEach(async (to, from, next) => {
  document.title = `${to.meta.title} | Waiter`;
  next();
});

export default router;
