import { createRouter, createWebHistory } from "vue-router"
import Homepage from "@/pages/Homepage.vue"
import Weapons from "@/pages/Weapons.vue"


const routes = [
    {
        path: "/",
        component: Homepage
    },
    {
        path: "/weapons",
        component: Weapons
    }
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;
