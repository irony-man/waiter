import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "",
    name: "home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/dashboard",
    meta: { transitionKey: "home", title: "Dashboard" },
    name: "dashboard-root",
    component: () => import("../views/dashboard/index.vue"),
    children: [
      {
        path: "",
        name: "dashboard",
        meta: { title: "Dashboard" },
        component: () => import("../views/dashboard/Chain.vue"),
      },
      {
        path: "restaurant/:uid",
        name: "restaurant",
        meta: { title: "Restaurant" },
        component: () => import("../views/dashboard/Restaurant.vue"),
      },
      {
        path: "category/:uid",
        name: "category",
        meta: { title: "Category" },
        component: () => import("../views/dashboard/Category.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(""),
  scrollBehavior() {
    return { top: 0 };
  },
  routes,
});

router.beforeEach(async (to, from, next) => {
  document.title = `${to.meta.title ? `${to.meta.title} | ` : ""}Waiter`;
  next();
});

export default router;
