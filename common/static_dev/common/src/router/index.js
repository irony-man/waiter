import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "",
    name: "home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/table/:tableUid",
    name: "table-root",
    meta: { title: "Table" },
    component: () => import("../views/table/index.vue"),
    children: [
      {
        path: "",
        name: "table",
        meta: { showNavCart: true, showNavOrder: true, title: "Table" },
        component: () => import("../views/table/TableView.vue"),
      },
      {
        path: "order",
        name: "table-order",
        meta: { showNavCart: true, title: "Order" },
        component: () => import("../views/table/OrderView.vue"),
      },
      {
        path: "category/:categoryUid",
        name: "table-category",
        meta: { showNavCart: true, showNavOrder: true, title: "Category" },
        component: () => import("../views/table/CategoryView.vue"),
      },
    ]
  },
  {
    path: "/dashboard",
    meta: { userNavigationBar: true, title: "Dashboard" },
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
        name: "dashboard-restaurant",
        meta: { title: "Restaurant" },
        component: () => import("../views/dashboard/Restaurant.vue"),
      },
      {
        path: "category/:uid",
        name: "dashboard-category",
        meta: { title: "Category" },
        component: () => import("../views/dashboard/Category.vue"),
      },
      {
        path: "order/:uid",
        name: "dashboard-order",
        meta: { title: "Order" },
        component: () => import("../views/dashboard/Order.vue"),
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
