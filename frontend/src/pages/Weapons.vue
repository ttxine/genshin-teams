<template>
  <div class="main-block__info _container">
    <p class="main-block__title--weapon _title">Weapons</p>
    <div class="main-block__weapon weapon">
      <form method="get" class="weapon__filter filter">
        <div class="filter__container">
          <div class="filter__type type">
            <ul class="type__list">
              <li class="type__item">
                <input type="checkbox" id="swords" name="swords">
                <label class="type__icon" for="swords">
                  <img src="@/assets/img/icons/swords.png">
                </label>
              </li>
              <li class="type__item">
                <input type="checkbox" id="claymores" name="claymores">
                <label class="type__icon" for="claymores">
                  <img src="@/assets/img/icons/claymores.png">
                </label>
              </li>
              <li class="type__item">
                <input type="checkbox" id="polearms" name="polearms">
                <label class="type__icon" for="polearms">
                  <img src="@/assets/img/icons/polearms.png">
                </label>
              </li>
              <li class="type__item">
                <input type="checkbox" id="catalysts" name="catalysts">
                <label class="type__icon" for="catalysts">
                  <img src="@/assets/img/icons/catalysts.png">
                </label>
              </li>
              <li class="type__item">
                <input type="checkbox" id="bows" name="bows">
                <label class="type__icon" for="bows">
                  <img src="@/assets/img/icons/bows.png">
                </label>
              </li>
            </ul>
          </div>
          <div class="filter__rarity">
            <ul class="rarity__list">
              <li class="rarity__item">
                <input type="checkbox" id="rarity1" name="rarity1">
                <label class="rarity__icon" for="rarity1">
                  1 ★
                </label>
              </li>
              <li class="rarity__item">
                <input type="checkbox" id="rarity2" name="rarity2">
                <label class="rarity__icon" for="rarity2">
                  2 ★
                </label>
              </li>
              <li class="rarity__item">
                <input type="checkbox" id="rarity3" name="rarity3">
                <label class="rarity__icon" for="rarity3">
                  3 ★
                </label>
              </li>
              <li class="rarity__item">
                <input type="checkbox" id="rarity4" name="rarity4">
                <label class="rarity__icon" for="rarity4">
                  4 ★
                </label>
              </li>
              <li class="rarity__item">
                <input type="checkbox" id="rarity5" name="rarity5">
                <label class="rarity__icon" for="rarity5">
                  5 ★
                </label>
              </li>
            </ul>
          </div>
          <p @click="createModalVisible = true" style="cursor: pointer" class="_link">
              Add Weapon
          </p>
        </div>
      </form>
      <Modal
        :showCreate="createModalVisible"
        :showDetail="detailModalVisible"
        :detailData="detailModalWeapon"
        v-if="createModalVisible || detailModalVisible"
        @close="createModalVisible = detailModalVisible = false; getWeapons()"
      />
      <div class="weapon__list">
        <div
          v-for="weapon in weapons"
          :key="weapon.id"
          @click="showWeaponDetail(weapon)"
          v-bind:class="`weapon__item--${weapon.core.rarity}-star`"
        >
          <div v-bind:class="`weapon__header--${weapon.core.rarity}-star`">
            <div class="weapon__type">
              <img src="@/assets/img/icons/swords.png">
            </div>
            <p class="weapon__title">{{ weapon.core.name }}</p>
          </div>
          <div class="weapon__container">
            <div class="weapon__menu">...</div>
            <div class="weapon__stats">
              <div class="weapon__stat stat">
                <p class="stat__prop">Base ATK:</p>
                <p class="stat__value">{{ Math.round(weapon.main_stat.value) }}</p>
              </div>
              <div class="weapon__stat stat">
                <p class="weapon__stat">{{ weapon.sub_stat.core.stat.toUpperCase() }}:</p>
                <p class="weapon__value">{{
                  weapon.sub_stat.core.stat.includes('%')
                    ? Math.round(weapon.sub_stat.value * 100) + '%'
                    : Math.round(weapon.sub_stat.value)
                }}</p>
              </div>
              <div class="weapon__stat stat">
                <p class="stat__prop">Level/Ascension:</p>
                <p class="stat__value">{{ weapon.level + '/' + weapon.ascension }}</p>
              </div>
              <div class="weapon__stat stat">
                <p class="weapon__stat">Refinement:</p>
                <p class="weapon__value">{{ weapon.refinement }}</p>
              </div>
            </div>
            <div class="weapon__image">
              <img :src="weapon.ascension < 2 ? apiURL + '/' + weapon.core.first_ascension_image : apiURL + '/' + weapon.core.second_ascension_image" alt="weapon">
            </div>
          </div>
        </div>
        <div class="weapon__add">
          <p @click="createModalVisible = true" class="_link _title">
            Add Weapon +
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-block__title--weapon {
	text-align: left;
	font-size: 32px;
}
input[type="checkbox"] {
	display: none;
}
.filter__container {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 5px 0;
	border-bottom: solid 1px #3A3A3A;
}
.type__list,
.rarity__list {
	display: flex;
	align-items: center;
}
.type__icon,
.rarity__icon {
	position: relative;
	display: block;
	cursor: pointer;
	padding: 0 5px;
	line-height: 30px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.filter__type,
.filter__rarity {
	margin-left: 5px;
	margin-right: 5px;
}
.filter__rarity {
	margin-right: auto;
}
.type__item,
.rarity__item {
	border-right: solid 1px #3A3A3A;
	height: 30px;
}
.type__item:last-child,
.rarity__item:last-child {
	border-right: none;
}
.type__icon img {
	width: 30px;
	height: 30px;
	object-fit: cover;
}
.type__icon::before,
.rarity__icon::before {
	content: "";
	position: absolute;
	display: block;
	background-color: #3A3A3A;
	width: 100%;
	height: 100%;
	top: 50%;
	left: 50%;
	transform: translateX(-50%) translateY(-50%) scale(0);
	opacity: .25;
	transition: all .25s;
}
:checked+.type__icon::before,
:checked+.rarity__icon::before {
	transform: translateX(-50%) translateY(-50%) scale(1.0);
}

.weapon__list {
	display: flex;
	justify-content: space-between;
	flex-wrap: wrap;
	align-items: center;
	margin: 15px;
}
.weapon__add {
  position: relative;
  width: 450px;
  height: 176px;
  padding: 25px 0;
}
.weapon__add > p {
  cursor: pointer;
  width: fit-content;
  position: absolute;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translateX(-50%) translateY(-50%);
  transition: all .25s;
}
.weapon__add > p:hover {
  transform: translateX(-50%) translateY(-50%) scale(1.25);
}
.weapon__item,
.weapon__item--1-star,
.weapon__item--2-star,
.weapon__item--3-star,
.weapon__item--4-star,
.weapon__item--5-star {
	position: relative;
	border-radius: 10px 10px 0 0;
	margin: 25px 0;
	width: 450px;
	filter: drop-shadow(0 0 3px rgba(58, 58, 58, 0.35));
	padding-bottom: 5px;
	overflow: hidden;
	cursor: pointer;
	transition: all .25s;
}
.weapon__item:hover,
.weapon__item--1-star:hover,
.weapon__item--2-star:hover,
.weapon__item--3-star:hover,
.weapon__item--4-star:hover,
.weapon__item--5-star:hover {
	transform: scale(1.05);
}
.weapon__header,
.weapon__header--1-star,
.weapon__header--2-star,
.weapon__header--3-star,
.weapon__header--4-star,
.weapon__header--5-star {
	display: flex;
	align-items: center;
	padding: 7px 5px;
}
.weapon__item--3-star,
.weapon__header--3-star {
  background: #86A8E7;
  background: -webkit-linear-gradient(to right, #91EAE4, #86A8E7);
  background: linear-gradient(to right, #91EAE4, #86A8E7);
}
.weapon__item--4-star,
.weapon__header--4-star {
  background: #DA22FF;
  background: -webkit-linear-gradient(to left, #9733EE, #DA22FF);
  background: linear-gradient(to left, #9733EE, #DA22FF);
}
.weapon__item--5-star,
.weapon__header--5-star {
  background: #f46b45;
  background: -webkit-linear-gradient(to right, #FFB75E, #f46b45);
  background: linear-gradient(to right, #FFB75E, #f46b45);
}
.weapon__type {
	filter: brightness(6.5);
	margin: 0 5px;
}
.weapon__title {
	color: white;
	font-size: 20px;
	margin: auto 5px;
}
.weapon__stats {
	flex: 0 1 225px;
	justify-self: start;
	padding: 10px 20px;
	line-height: 28px;
	font-size: 16px;
}
.weapon__stat {
	display: flex;
  flex-wrap: wrap;
	justify-content: space-between;
}
.weapon__container {
	display: flex;
	align-items: center;
  flex-wrap: wrap;
	background-color: #F4F0E9;
	box-sizing: content-box;
}
.weapon__menu {
	font-size: 32px;
	padding: 7px 15px;
	line-height: 0;
	margin-bottom: 16px;
	cursor: pointer;
}
.weapon__image {
	position: relative;
	align-self: flex-end;
	margin-left: auto;
	width: 160px;
	filter: drop-shadow(0 0 3px rgba(58, 58, 58, 0.65));
	z-index: 2;
}
.weapon__image img {
	position: absolute;
	bottom: 0;
	display: block;
	max-width: 100%;
	z-index: 2;
}
@media (max-width: 767.98px) {
  .weapon__filter {
    display: none;
  }
}
@media (max-width: 429.98px) {
  .weapon__image {
    opacity: .5;
  }
  .weapon__menu {
    display: none;
  }
}
</style>

<script>
import Modal from '@/components/weapons/Modal.vue'

export default {
  data() {
    return {
      weapons: [],
      createModalVisible: false,
      detailModalVisible: false,
      detailModalWeapon: null,
      apiUrl: ''
    }
  },
  components: {
    Modal
  },
  mounted() {
    this.apiURL = process.env.VUE_APP_API_PREFIX;
    this.getWeapons();
  },
  methods: {
    getWeapons() {
      try {
        this.weapons = JSON.parse(localStorage.getItem('weapons'));
      } catch(e) {
        localStorage.removeItem('weapons');
        console.error(e);
      }
    },
    showWeaponDetail(weapon) {
        this.detailModalVisible = true,
        this.detailModalWeapon = weapon
    }
  }
}
</script>