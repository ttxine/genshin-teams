<template>
    <div class="main-block__image _ibg">
        <img src='@/assets/img/cover.png' alt="cover">
    </div>
    <div class="main-block__header _container">
        <p class="main-block__logo _logo _unselectable">Genshin Teams</p>
        <p class="main-block__description _unselectable">
            is a tool providing an editor of weapons, artifacts and characters that allows you plan and share your own teams
        </p>
        <p class="main-block__text scroll"></p>
    </div>
    <div class="main-block__info _container">
        <p class="main-block__text">Create your own team by several steps</p>
        <div class="main-block__steps step">
            <div class="steps__item">
                <div class="steps__icon">
                    <img src='@/assets/img/icons/weapon.png' alt="weapon-icon">
                </div>
                <p class="steps__title _title">Weapons</p>
            </div>
            <div class="steps__item">
                <div class="steps__icon">
                    <img src='@/assets/img/icons/artifact.png' alt="artifact-icon">
                </div>
                <p class="steps__title _title">Artifacts</p>
            </div>
            <div class="steps__item">
                <div class="steps__icon">
                    <img src='@/assets/img/icons/character.png' alt="character-icon">
                </div>
                <p class="steps__title _title">Characters</p>
            </div>
        </div>
    </div>
    <p class="main-block__text scroll"></p>
    <div class="main-block__info _container">
        <p class="main-block__title _title">Getting Started</p>
        <div class="main-block__menu menu">
            <router-link to="/weapons">
                <div class="menu__item">
                    <div class="menu__title _title">Weapons</div>
                    <div class="menu__icon">
                        <img src="@/assets/img/icons/arw.png" alt="arrow">
                    </div>
                    <div class="menu__card">
                        <div class="menu__image">
                            <img src="@/assets/img/menu/weapons.png" alt="weapons">
                        </div>
                        <div class="menu__bg--weapons"></div>
                    </div>
                </div>
            </router-link>
            <a href="#">
                <div class="menu__item">
                    <div class="menu__title _title">Characters</div>
                    <div class="menu__icon">
                        <img src="@/assets/img/icons/arw.png" alt="arrow">
                    </div>
                    <div class="menu__card">
                        <div class="menu__image">
                            <img src="@/assets/img/menu/characters.png" alt="characters">
                        </div>
                        <div class="menu__bg--characters"></div>
                    </div>
                </div>
            </a>
            <a href="#">
                <div class="menu__item">
                    <div class="menu__title _title">Artifacts</div>
                    <div class="menu__icon">
                        <img src="@/assets/img/icons/arw.png" alt="arrow">
                    </div>
                    <div class="menu__card">
                        <div class="menu__image">
                            <img src="@/assets/img/menu/artifacts.png" alt="artifacts">
                        </div>
                        <div class="menu__bg--artifacts"></div>
                    </div>
                </div>
            </a>
            <a href="#">
                <div class="menu__item">
                    <div class="menu__title _title">Teams</div>
                    <div class="menu__icon">
                        <img src="@/assets/img/icons/arw.png" alt="arrow">
                    </div>
                    <div class="menu__card">
                        <div class="menu__image">
                            <img src="@/assets/img/menu/teams.png" alt="teams">
                        </div>
                        <div class="menu__bg--teams"></div>
                    </div>
                </div>
            </a>
        </div>
    </div>
    <p class="main-block__text scroll"></p>
    <div class="main-block__info _container">
        <p class="main-block__title _title">Support Us</p>
        <div class="main-block__patreon patreon">
            <div class="patreon__logo">
                <img src="@/assets/img/icons/patreon.png">
            </div>
            <div class="patreon__inner">
                <div class="patreon__text">
                    Genshin Teams is a project that has absorbed hundreds of hours of work from one developer. I'm sure he'll be happy if you support him on Patreon.
                </div>
                <a href="https://www.patreon.com/" class="patreon__btn">Become a Patron</a>
            </div>
        </div>
    </div>
</template>

<style scoped>
.scroll {
	position: relative;
}
.scroll::after {
	content: "";
	position: relative;
	display: block;
	width: 1px;
	height: 200px;
	left: 50%;
	transform: translateX(-50%);
	background-color: #B2B2B2;
}
.main-block__steps {
	padding: 50px 0;
	display: flex;
	justify-content: space-evenly;
	font-size: 14px;
}
.steps__item {
	width: fit-content;
	width: -moz-fit-content;
	flex: 0 0 130px;
}
.steps__icon {
	position: relative;
	margin: 0 auto;
	background-color: #3A3A3A;
	border-radius: 15px;
	width: 70px;
	height: 80px;
}
.steps__icon img {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translateX(-50%) translateY(-50%);
	width: 48px;
	height: 48px;
}
.steps__title {
	margin: 10px auto;
	text-align: center;
}
.main-block__menu {
	display: flex;
	flex-wrap: wrap;
	justify-content: space-evenly;
	margin: 50px auto;
}
.main-block__menu a {
	padding: 50px;
}
.main-block__menu a:hover .menu__icon {
	width: 68px;
	right: -25px;
	transform: translateY(-55%);
}
.main-block__menu a:hover .menu__title {
	font-size: 34px;
	left: 20px;
	transform: translateX(-10%) translateY(-55%);
}
.main-block__menu a:hover .menu__image img {
	transform: scale(107%);
}
.menu__item {
	position: relative;
	width: 400px;
	padding-left: 15px;
}
.menu__title {
	position: absolute;
	font-size: 32px;
	left: 0;
	transform: translateX(-10%) translateY(-45%);
	z-index: 2;
	transition: all .25s;
}
.menu__icon {
	position: absolute;
	width: 64px;
	height: 32px;
	right: 0;
	transform: translateY(-45%);
	z-index: 1;
	transition: all .25s;
}
.menu__card {
	padding: 0 15px;
}
.menu__image {
	position: absolute;
	height: 265px;
	padding-top: 15px;
	padding-left: 15px;
	top: -15px;
	width: 100%;
	overflow: hidden;
	z-index: 1;
}
.menu__image img {
	transition: all .25s;
}
.menu__bg,
.menu__bg--weapons,
.menu__bg--characters,
.menu__bg--artifacts,
.menu__bg--teams {
	position: relative;
	width: 300px;
	height: 250px;
	transform: skew(-25deg);
	border-radius: 50% 10% 50% 10%;
	background: #DA22FF;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to right, #9733EE, #DA22FF);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to right, #9733EE, #DA22FF); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
	z-index: 0;
}
.menu__bg--weapons {
	background: #DA22FF;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to left, #9733EE, #DA22FF);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to left, #9733EE, #DA22FF); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.menu__bg--characters {
	background: #EF3B36;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to bottom, #F9F6F2, #EF3B36);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to bottom, #F9F6F2, #EF3B36); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.menu__bg--artifacts {
	background: #f46b45;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to right, #FFB75E, #f46b45);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to right, #FFB75E, #f46b45); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.menu__bg--teams {
	background: #7F7FD5;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to right, #91EAE4, #86A8E7);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to right, #91EAE4, #86A8E7); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.main-block__patreon {
	display: flex;
	flex-wrap: wrap;
	justify-content: space-evenly;
	align-items: flex-start;
	margin: 100px auto;
}
.patreon__logo {
	max-width: 128px;
	max-height: 128px;
}
.patreon__text {
	width: 512px;
}
.patreon__btn {
	color: white;
	display: block;
	width: fit-content;
	border-radius: 50px;
	margin: 15px 0;
	padding: 10px 15px;
	background-color: #FF424D;
	transition: all .25s;
}
.patreon__btn:hover {
	background-color: #141518;
}
</style>

<script>
export default {
    created() {
        this.$root.$data.headerIsWhite = true;
    },
    mounted() {
        this.bgImage = document.querySelector('.main-block__image');

        document.addEventListener('scroll', this.handleScroll);
    },
    methods: {
        handleScroll() {
            let positionTop = this.bgImage.getBoundingClientRect().top + this.bgImage.clientHeight;

            if (positionTop <= 0) {
                this.$root.$data.headerIsWhite = false;
            } else {
                this.$root.$data.headerIsWhite = true;
            }
        }
    },
    unmounted() {
        document.removeEventListener('scroll', this.handleScroll);
        this.$root.$data.headerIsWhite = false;
    }
}
</script>
