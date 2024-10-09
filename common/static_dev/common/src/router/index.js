import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "",
    name: "home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/table/:uid",
    name: "table",
    meta: { title: "Table" },
    component: () => import("../views/table/TableView.vue"),
  },
  {
    path: "/table/:tableUid/category/:categoryUid",
    name: "table-category",
    meta: { title: "Category" },
    component: () => import("../views/table/CategoryView.vue"),
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
