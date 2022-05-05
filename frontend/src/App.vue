<template>
  <div class="wrapper">
    <Header
		:isWhite="headerIsWhite"
	/>
    <main class="main">
		<router-view></router-view>
    </main>
    <Footer/>
  </div>
</template>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
}
ul,
ol {
  padding: 0;
}
body,
main,
h1,
h2,
h3,
h4,
p,
ul,
ol,
li{
  margin: 0;
}
body {
  min-height: 100vh;
  scroll-behavior: smooth;
  text-rendering: optimizeSpeed;
  line-height: 1.5;
}
ul,
ol {
  list-style: none;
}
a {
	color: inherit;
  text-decoration: none;
}
img {
  max-width: 100%;
  display: block;
}
input,
button,
textarea,
select {
  font: inherit;
}
button {
	border: none;
  cursor: pointer;
  background: transparent;
}


body {
	font-family: 'Comfortaa', cursive;
	background-color: #F9F6F2;
	color: #3A3A3A;
}
main {
	min-height: calc(100vh - 317px);
}
input {
	width: 100%;
}
.wrapper {
	display: flex;
	flex-direction: column;
}

._container {
	max-width: 1000px;
	padding: 0 20px;
	margin: 0 auto;
	box-sizing: content-box;
}
._logo {
	font-family: 'Cinzel', serif;
	font-size: 25px;
	line-height: 90%;
}
._ibg {
	position: relative;
}
._ibg img {
	position: absolute;
	width: 100%;
	left: 50%;
	transform: translateX(-50%);
  pointer-events: none;
  object-fit: cover;
}
._link {
	position: relative;
}
._link::after {
	content: "";
	display: block;
	position: absolute;
	width: 0;
	transition: all .25s;
	height: 1px;
}
._link:hover::after {
	width: 100%;
}
._form {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	align-items: center;
}
._title {
	font-family: 'Cinzel', serif;
	font-size: 20px;
}
._unselectable {
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
._input {
	border: solid 1px #C7C7C7;
	border-radius: 5px;
	padding: 10px;
	font-size: 16px;
}
._input:focus-visible {
	border: solid 1px #A3A3A3;
	outline: none;
}

.main {
	width: 100%;
}
.main-block__image {
	min-height: 600px;
	padding: 0 20px;
	margin: 0 auto;
  pointer-events: none;
  box-sizing: content-box;
  z-index: 0;
  opacity: .9;
  overflow: hidden;
}
.main-block__logo {
	position: absolute;
	font-size: 80px;
	left: 50%;
	top: 580px;
	transform: translateX(-50%);
	text-align: center;
}
.main-block__header {
	margin: 0 auto;
	padding: 150px 20px 10px 20px;
	background-color: #F9F6F2;
}
.main-block__description {
	position: absolute;
	max-width: 450px;
	font-size: 10px;
	line-height: 10px;
	left: 50%;
	top: 660px;
	transform: translateX(-50%);
	text-align: center;
}
.main-block__info {
	padding: 50px 0;
}
.main-block__title,
.main-block__title--weapon {
	text-align: center;
	margin: 75px auto;
	font-size: 48px;
}
.main-block__text {
	text-align: center;
	margin: 50px auto;
}

@media (max-width: 1440px) {
	._container {
		max-width: 1000px;
	}
	.main-block__logo {
		width: fit-content;
	}
}
@media (max-width: 991.98px) {
	._container {
		max-width: 750px;
	}
	.main-block__image {
		min-height: 350px;
	}
	.main-block__logo {
		top: 340px;
		font-size: 48px;
	}
	.main-block__description {
		max-width: 175px;
		line-height: 8px;
		top: 380px;
		font-size: 5px;
	}
}
</style>

<script>
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"

export default {
  components: {
    Header, Footer
  },
  data() {
	  return {
		  headerIsWhite: false
	  }
  },
  created() {
	  this.headerIsWhite = false;
  }
}
</script>