import { createRouter, createWebHashHistory } from "vue-router"
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
    history: createWebHashHistory(),
    routes
})

export default router;
