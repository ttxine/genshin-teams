<template>
    <transition name="rotate">
        <img v-if="!showHeader" v-on:click="showHeader = true" v-bind:class="isWhite ? 'header__open-icon--white' : 'header__open-icon--dark'" src="@/assets/img/icons/open.png">
    </transition>
    <transition name="display">
        <header v-if="showHeader" class="header">
            <div class="header__container _container">
                <img v-if="showHeader" v-on:click="showHeader = false" class="header__close-icon" src="@/assets/img/icons/close.png">
                <router-link to="/" v-bind:style="isWhite ? 'color: #fff' : 'color: #3A3A3A'" class="header__logo _logo _unselectable">
                    Genshin Teams
                </router-link>
                <nav class="header__nav nav">
                    <ul class="nav__list">
                        <li @click="handleClientRect()" v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                            <router-link to="/" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Home</router-link>
                        </li>
                        <li @click="handleClientRect()" v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                            <router-link to="/weapons" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Weapons</router-link>
                        </li>
                        <li @click="handleClientRect()" v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                            <a href="#" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Artifacts</a>
                        </li>
                        <li @click="handleClientRect()" v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                            <a href="#" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Characters</a>
                        </li>
                        <li @click="handleClientRect()" v-bind:class="isWhite ? 'nav__item--white' : 'nav__item--dark'" class="_link">
                            <a href="#" v-bind:class="isWhite ? 'nav__link--white' : 'nav__link--dark'">Teams</a>
                        </li>
                    </ul>
                </nav>
                <div @click="showSignin = true" v-bind:class="isWhite ? 'signup__btn--white' : 'signup__btn--dark'" class="header__signup">SIGN IN</div>
            </div>
        </header>
    </transition>
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
    .header__close-icon {
        display: none;
    }
    .header__open-icon
    .header__open-icon--white,
    .header__open-icon--dark {
        display: none;
    }

    .display-enter-active, .display-leave-active {
        transition: all .5s;
    }
    .display-enter-from, .display-leave-to {
        transform: translateX(-100%);
        transform-origin: 0;
    }
    .rotate-enter-active, .rotate-leave-active {
        transition: all .25s;
    }
    .rotate-enter-from, .rotate-leave-to {
        transform: rotate(90deg);
        opacity: 0;
    }

    @media (max-width: 766.98px) {
        .header__open-icon,
        .header__open-icon--white,
        .header__open-icon--dark {
            position: fixed;
            display: block;
            width: 36px;
            height: 32px;
            left: 20px;
            top: 20px;
            transition: all .25s;
            z-index: 100;
        }
        .header__open-icon--white {
            filter: brightness(5);
        }
        .header__open-icon--dark {
            filter: brightness(0);
        }
        .header__close-icon {
            display: block;
            width: 16px;
            height: 16px;
            margin: 30px 15px; 
        }
        header {
            width: 0;
        }
        .header__container {
            flex-direction: column;
            margin-left: 0;
            padding-right: 25px;
            width: fit-content;
            width: -moz-fit-content;
            background-color: #F4F0E9;
            height: 100vh;
            align-items: flex-start;
            justify-content: flex-start;
        }
        .nav__list {
            padding: 15px;
            flex-direction: column;
            font-family: 'Cinzel', serif;
            font-size: 20px;
        }
        .nav__list > li {
            width: fit-content;
            width: -moz-fit-content;
            margin: 20px 0;
        }
        .nav__item--white::after {
            background-color: #3A3A3A;
        }
        .nav__link--white {
            color: #3A3A3A;
        }
        .header__logo {
            display: none;
        }
        .header__signup {
            display: none;
        }
    }
</style>

<script>
import Signin from "@/components/Signin.vue"

export default {
    components: {
        Signin
    },
    mounted() {
        this.handleClientRect();
    },
    methods: {
        handleClientRect() {
            if (document.documentElement.clientWidth > 766.98)
                this.showHeader = true;
            else
                this.showHeader = false;
        }
    },
    data() {
        return {
            showSignin: false,
            showHeader: false
        }
    },
    props: ['isWhite']
}
</script>