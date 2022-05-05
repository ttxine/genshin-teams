<template>
  <footer class="footer">
    <div class="footer__container _container">
      <div class="footer__list">
        <div class="footer__item">
          <p class="footer__title _title">Genshin Teams</p>
        </div>
        <div class="footer__item">
          <p class="footer__title _title">Main</p>
          <ul>
            <li class="_link">
              <router-link to="/">Home</router-link>
            </li>
            <li class="_link">
              <router-link to="/weapons">Weapons</router-link>
            </li>
            <li class="_link">
              <a href="#">Artifacts</a>
            </li>
            <li class="_link">
              <a href="#">Characters</a>
            </li>
            <li class="_link">
              <a href="#">Teams</a>
            </li>
          </ul>
        </div>
        <div class="footer__item">
          <p class="footer__title _title">GitHub</p>
          <ul>
            <li class="_link">
              <a href="https://github.com/Ryaku-s/genshin-teams">Repository</a>
            </li>
          </ul>
        </div>
        <div class="footer__item">
          <p class="footer__title _title">Social</p>
          <ul>
            <li class="_link">
              <a href="#">Discord</a>
            </li>
          </ul>
        </div>
        <div class="footer__item">
          <p class="footer__title _title">Support Us</p>
          <ul>
            <li class="_link">
              <a href="#">Patreon</a>
            </li>
          </ul>
        </div>
      </div>
      <p class="footer__text">Genshin Teams does not cooperate with miHoYo. <span class="footer__version">Version: 0.1.0</span></p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
	margin-top: 50px;
	background-color: #F4F0E9;
	font-size: 14px;
}
.footer__container {
	position: relative;
}
.footer__list {
	padding: 25px 0;
	display: flex;
	justify-content: space-between;
	border-bottom: solid 1px #B2B2B2;
}
.footer__item ul > li {
	margin: 5px 0;
	width:fit-content;
	width: -moz-fit-content;
}
.footer__item ul > li::after {
	background-color: #3A3A3A;
}
.footer__text {
	padding: 15px 0;
}
.footer__version {
	position: absolute;
	right: 20px;
}
</style>

<script>
export default {
  
}
</script>