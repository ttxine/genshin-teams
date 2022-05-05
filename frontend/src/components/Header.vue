<template>
    <header class="header">
        <div class="header__container _container">
            <a href="#" v-bind:style="isWhite ? 'color: #fff' : 'color: #3A3A3A'" class="header__logo _logo _unselectable">
                Genshin Teams
            </a>
            <nav class="header__nav nav">
                <ul class="nav__list">
                    <li v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                        <router-link to="/" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Home</router-link>
                    </li>
                    <li v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                        <router-link to="/weapons" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Weapons</router-link>
                    </li>
                    <li v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                        <a href="#" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Artifacts</a>
                    </li>
                    <li v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                        <a href="#" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Characters</a>
                    </li>
                    <li v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                        <a href="#" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Teams</a>
                    </li>
                </ul>
            </nav>
            <div @click="showSignin = true" v-bind:class="isWhite ? 'signup__btn--white' : 'signup__btn--dark'" class="header__signup">SIGN IN</div>
        </div>
    </header>
    <Signin
		v-if="showSignin"
	/>
</template>

<style scoped>
    .header {
        position: fixed;
        width: 100%;
        left: 0;
        top: 0;
        z-index: 50;
        transition: all .25s;
        color: #3a3a3a;
    }
    .header__container {
        display: flex;
        max-width: 1250px;
        min-height: 80px;
        align-items: center;
        justify-content: space-between;
    }
    .header__logo {
        margin-right: 15px;
        text-align: center;
        transition: all .25s;
    }
    .header__signup {
        font-size: 14px;
        flex: 0 0 90px;
        padding: 0 15px;
        margin: 0 15px;
        text-align: center;
        color: #3A3A3A;
        border-radius: 50px;
        background-color: white;
        transition: all .25s;
        cursor: pointer;
    }
    .signup__btn--white {
        color: #3a3a3a;
        background-color: white;
    }
    .signup__btn--white:hover {
        color: white;
        background-color: #3a3a3a;
    }
    .signup__btn--dark {
        color: white;
        background-color: #3a3a3a;
    }
    .signup__btn--dark:hover {
        color: #3a3a3a;
        background-color: white;
    }
    .header__nav {
        margin-right: auto;
        font-size: 14px;
    }

    .nav__list {
        display: flex;
        justify-content: space-between;
    }
    .nav__item,
    .nav__item--white,
    .nav__item--dark {
        margin: 0 15px;
        transition: all .25s;
    }
    .nav__link,
    .nav__link--white,
    .nav__link--dark {
        transition: all .25s;
    }
    .nav__item--white::after {
        background-color: white;
    }
    .nav__link--white {
        color: white;
    }
    .nav__item--dark::after {
        background-color: #3A3A3A;
    }
    .nav__link--dark {
        color: #3A3A3A;
    }
</style>

<script>
import Signin from "@/components/Signin.vue"

export default {
    components: {
        Signin
    },
    data() {
        return {
            showSignin: false
        }
    },
    props: ['isWhite']
}
</script>