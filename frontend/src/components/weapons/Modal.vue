<template>
    <div class="main-block__create create">
        <div class="create__container">
            <div class="create__ingame-item ingame-item">
                <div class="ingame-item__container">
                    <img v-on:click="$emit('close')" class="close-icon" src="@/assets/img/icons/close.png">
                    <New
						v-if="showCreate"
					/>
					<Detail
						v-if="showDetail"
						:detailData="detailData"
					/>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.close-icon {
	position: absolute;
	top: 5px;
	right: 5px;
	width: 16px;
	height: 16px;
	margin: 16px;
	cursor: pointer;
}

.main-block__create {
	position: fixed;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
	z-index: 100;
	background-color: rgba(0, 0, 0, .25);
}
.create__container {
	position: fixed;
	top: 50%;
	transform: translateY(-50%);
	width: 100%;
	max-height: 100%;
}
.ingame-item__container {
	position: relative;
	background-color: #F9F6F2;
	border-radius: 5px;
	max-width: 800px;
	margin: 0 auto;
	padding: 60px 30px;
}
</style>


<script>
import New from '@/components/weapons/New.vue'
import Detail from '@/components/weapons/Detail.vue'

export default {
	props: [
		'showCreate', 'showDetail', 'detailData'
	],
    components: {
        New, Detail
    }
}
</script>
