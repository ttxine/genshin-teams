<template>
    <div class="ingame-item__main">
        <form method="get">
            <div class="ingame-item-form _form">
                <div class="ingame-item-form__level-input level-input">
                    <div class="level-input__container">
                        <label class="_label" for="level">
                            Level
                        </label>
                        <input
                            v-bind:value="level"
                            @input="inputLevel"
                            class="_level-input _input"
                            step="1"
                            :max="90"
                            maxlength="2"
                            minlength="1"
                            type="number"
                            placeholder=""
                            id="level"
                            name="level"
                        >
                        <label class="_label" for="ascension">
                            Ascension
                        </label>
                        <input
                            v-bind:value="ascension"
                            @input="inputAscension"
                            class="_level-input _input"
                            step="1"
                            type="number"
                            placeholder=""
                            id="ascension"
                            name="ascension"
                        >
                    </div>
                </div>
                <div class="ingame-item-form__refinement-input refinement-input">
                    <div class="refinement-input__container">
                        <label class="_label" for="refinement">
                            Refinement
                        </label>
                        <input class="_level-input _input" min="1" max="90" step="1" :value="weapon.refinement" type="number" placeholder="" id="refinement" name="refinement">
                    </div>
                </div>
            </div>
        </form>
        <div class="main__detail">
            <div class="main__image">
                <img :src="weaponImage" alt="weapon">
            </div>
            <div class="main__info">
                <p class="main__title _title">Main Stats</p>
                <div class="main__stats">
                    <div class="main__stat stat">
                        <p class="stat__prop">Base ATK:</p>
                        <p class="stat__value">{{ Math.round(weapon.main_stat.value) }}</p>
                    </div>
                    <div class="main__stat stat">
                        <p class="stat__prop">{{ weapon.sub_stat.core.stat.toUpperCase() }}:</p>
                        <p class="stat__value">{{ Math.round(weapon.sub_stat.value) }}</p>
                    </div>
                </div>
            </div>
        </div>
        <p style="font-size: 30px; margin-top: 20px;" class="main__title _title">{{ weapon.core.name }}</p>
        <div class="main__info">
            <p class="main__title _title">{{ weapon.passive_ability.core.name }}</p>
            <p class="main__description">
                {{ weapon.passive_ability.description }}
            </p>
        </div>
    </div>
</template>

<style scoped>
.level-input__container,
.refinement-input__container {
	display: flex;
	align-items: center;
	padding: 5px 10px;
	border-radius: 7px;
	background-color: #3A3A3A;
	color: #F9F6F2;
}
._level-input {
	width: 65px;
	padding: 0 0 0 25px;
	border: none;
	color: #FFF;
	background-color: #3A3A3A;
}
._level-input:focus-visible {
	border: none;
}
._ascension-input {
	width: 65px;
	width: 100%;
	border: none;
	color: #FFF;
	background-color: #3A3A3A;
	padding: 0 0 0 25px;
}
._ascension-input:focus-visible {
	border: none;
}
.ingame-item__title {
	font-size: 32px;
	text-align: center;
}
.ingame-item-form {
	display: flex;
	flex-direction: row;
	padding: 7px;
	border-bottom: solid 1px #3A3A3A;
}
.ingame-item__main > div {
	padding: 10px 0;
}
.main__title {
	font-size: 24px;
}
.main__detail {
	display: flex;
}
.main__detail > .main__info {
	margin-left: 25px;
}
.main__image {
	flex: 0 0 160px;
	position: relative;
	width: 160px;
	height: 160px;
	overflow: hidden;
	border-radius: 10px;
	background: #DA22FF;  /* fallback for old browsers */
	background: -webkit-linear-gradient(to left, #9733EE, #DA22FF);  /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to left, #9733EE, #DA22FF); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.main__image img {
	position: absolute;
	top: 50%;
	left: 50%;
	height: 180px;
	transform: translateX(-50%) translateY(-50%);
	object-fit: cover;
}
.main__stats {
	justify-self: start;
	line-height: 28px;
	font-size: 16px;
}
.stat__value {
	font-size: 24px;
}
</style>

<script>
import axios from 'axios'

export default {
    props: [
        'detailData'
    ],
    data() {
        return {
            weapon: this.detailData,
            weaponImage: null,
            level: this.detailData.level,
            ascension: this.detailData.ascension
        }
    },
    methods: {
        async inputLevel(event) {
            try {
                let level = event.target.value;
                let ascension = this.ascension;

                if (level == '')
                    level = 1

                if (level <= 20) {
                    ascension = 0;
                } else if (level > 20 && level <= 40) {
                    ascension = 1;
                } else if (level > 40 && level <= 50){
                    ascension = 2;
                } else if (level > 50 && level <= 60){
                    ascension = 3;
                } else if (level > 60 && level <= 70){
                    ascension = 4;
                } else if (level > 70 && level <= 80){
                    ascension = 5;
                } else if (level > 80 && level <= 90){
                    ascension = 6;
                } else if (level > 90) {
                    level = 90;
                    ascension = 6
                }

                const response = await axios.post('http://localhost:8000/api/v1/weapons', {
                    core: this.weapon.core.id,
                    level: level,
                    ascension: ascension,
                    refinement: this.weapon.refinement
                })
                const weapon = response.data;

                try{
                    let localWeapons = JSON.parse(localStorage.getItem('weapons'));

                    for (let i = 0; i < localWeapons.length; i++) {
                        if (localWeapons[i].key == this.weapon.key) {
                            weapon['key'] = this.weapon.key;
                            localWeapons[i] = weapon;

                            this.weapon = weapon;
                            this.level = weapon.level;
                            this.ascension = weapon.ascension;
                        }
                    }
                    localStorage.setItem(
                        'weapons',
                        JSON.stringify(localWeapons)
                    );
                } catch(e) {
                    localStorage.removeItem('weapons');
                }
            } catch(e) {
                this.weapon = this.detailData;
            }
        }
    },
    mounted() {
        if (this.weapon.ascension < 2) {
            this.weaponImage = `http://localhost:8000/${this.weapon.core.first_ascension_image}`
        } else {
            this.weaponImage = `http://localhost:8000/${this.weapon.core.second_ascension_image}`
        }
    }
}
</script>
