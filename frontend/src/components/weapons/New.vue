<template>
    <div class="ingame-item__core core">
        <form method="get" class="weapon__filter filter">
            <div class="filter__container">
                <div class="filter__type type">
                    <ul class="type__list">
                        <li class="type__item">
                            <input type="checkbox" id="core-swords" name="core-swords">
                            <label class="type__icon" for="core-swords">
                                <img src="@/assets/img/icons/swords.png">
                            </label>
                        </li>
                        <li class="type__item">
                            <input type="checkbox" id="core-claymores" name="core-claymores">
                            <label class="type__icon" for="core-claymores">
                                <img src="@/assets/img/icons/claymores.png">
                            </label>
                        </li>
                        <li class="type__item">
                            <input type="checkbox" id="core-polearms" name="core-polearms">
                            <label class="type__icon" for="core-polearms">
                                <img src="@/assets/img/icons/polearms.png">
                            </label>
                        </li>
                        <li class="type__item">
                            <input type="checkbox" id="core-catalysts" name="core-catalysts">
                            <label class="type__icon" for="core-catalysts">
                                <img src="@/assets/img/icons/catalysts.png">
                            </label>
                        </li>
                        <li class="type__item">
                            <input type="checkbox" id="core-bows" name="core-bows">
                            <label class="type__icon" for="core-bows">
                                <img src="@/assets/img/icons/bows.png">
                            </label>
                        </li>
                    </ul>
                </div>
                <div class="filter__rarity">
                    <ul class="rarity__list">
                        <li class="rarity__item">
                            <input type="checkbox" id="core-rarity1" name="core-rarity1">
                            <label class="rarity__icon" for="core-rarity1">
                                1 ★
                            </label>
                        </li>
                        <li class="rarity__item">
                            <input type="checkbox" id="core-rarity2" name="core-rarity2">
                            <label class="rarity__icon" for="core-rarity2">
                                2 ★
                            </label>
                        </li>
                        <li class="rarity__item">
                            <input type="checkbox" id="core-rarity3" name="core-rarity3">
                            <label class="rarity__icon" for="core-rarity3">
                                3 ★
                            </label>
                        </li>
                        <li class="rarity__item">
                            <input type="checkbox" id="core-rarity4" name="core-rarity4">
                            <label class="rarity__icon" for="core-rarity4">
                                4 ★
                            </label>
                        </li>
                        <li class="rarity__item">
                            <input type="checkbox" id="core-rarity5" name="core-rarity5">
                            <label class="rarity__icon" for="core-rarity5">
                                5 ★
                            </label>
                        </li>
                    </ul>
                </div>
                <div class="filter__order-by"></div>
            </div>
        </form>
        <div class="core__list">
            <div v-for="core in weaponCores" @click="createWeapon(core.id);" :key="core.id" :title="core.name" class="core__item">
                <div class="core__icon">
                    <img :src="'http://localhost:8000/' + core.first_ascension_image">
                </div>
                <div class="core__rarity">
                    <img :src="require(`@/assets/img/icons/rarity/rarity-${core.rarity}.png`)">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
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

.core__list {
	padding: 25px 0;
	display: flex;
}
.core__item {
	display: flex;
	flex-direction: column;
	width: 100px;
	height: 130px;
	background-color: #F4F0E9;
	border-radius: 10px;
	margin: 10px;
	filter: drop-shadow(0 0 3px rgba(58, 58, 58, 0.65));
	overflow: hidden;
	cursor: pointer;
	transition: all .25s;
}
.core__item:hover {
	transform: scale(1.05);
}
.core__icon {
	position: relative;
	overflow: hidden;
	height: 110px;
	border-radius: 0 0 20px 0;
	background: #DA22FF;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to left, #9733EE, #DA22FF);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to left, #9733EE, #DA22FF); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.core__icon img {
	position: absolute;
	max-width: 160px;
	height: 160px;
	top: 50%;
	left: 50%;
	transform: translateX(-50%) translateY(-50%);
	object-fit: cover;
}
.core__rarity {
	position: relative;
}
.core__rarity img {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translateX(-50%) translateY(-50%) scale(1);
	filter: drop-shadow(0 0 2px rgba(58, 58, 58, 0.75));
}
</style>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            weaponCores: []
        }
    },
    mounted() {
        this.fetchWeaponCores();
    },
    methods: {
        async fetchWeaponCores() {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/weapon-cores?weapon_types=sw&weapon_types=cl&weapon_types=po&weapon_types=ca&weapon_types=bo&rarities=1&rarities=2&rarities=3&rarities=4&rarities=5');
                this.weaponCores = response['data'];
            }
            catch (e) {
                console.log(e);
            }
        },
        async createWeapon(core) {
            await axios.post('http://localhost:8000/api/v1/weapons', {
                core: core,
                level: 1,
                ascension: 0,
                refinement: 1
            })
            .then(function(response) {
                const weapon = response.data;

                if (!localStorage.hasOwnProperty('weapons')) {
                    weapon['key'] = 0;
                    localStorage.setItem('weapons', JSON.stringify([weapon]));
                } else {
                    try{
                        let weapons = JSON.parse(localStorage.getItem('weapons'));
                        weapon['key'] = weapons.length
                        weapons.push(weapon);

                        localStorage.setItem(
                            'weapons',
                            JSON.stringify(weapons)
                        );
                    } catch(e) {
                        localStorage.removeItem('weapons');
                    }
                }
            })
            .catch(function(error) {
                console.error(error);
            })

            this.$parent.$emit('close');
        }
    }
}
</script>