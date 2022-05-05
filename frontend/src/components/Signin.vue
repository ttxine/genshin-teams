<template>
    <div class="gt-account">
        <div class="gt-account__container">
            <div class="gt-account__login login">
                <div class="login__container _container">
                    <img @click="this.$parent.$data.showSignin = false" class="close-icon" src="@/assets/img/icons/close.png">
                    <p class="login__title _title">Sign In</p>
                    <form class="gt-account-form _form" method="post">
                        <div class="gt-account-form__input input">
                            <div class="input__container _container">
                                <label class="_label" for="login">
                                    Username
                                    <input class="_input" type="text" placeholder="Your username" name="username">
                                </label>
                            </div>
                        </div>
                        <div class="gt-account-form__input input">
                            <div class="input__container">
                                <label class="_label" for="password">
                                    Password
                                    <input class="_input" type="password" placeholder="Your password" name="password">
                                </label>
                            </div>
                        </div>
                        <div class="gt-account-form__btn">
                            <button class="login__btn" type="submit">Sign In</button>
                        </div>
                        <div class="gt-account-form__support">
                            <div class="gt-account-form__link _link">
                                <a href="#">Forgot password?</a>
                            </div>
                            <div class="gt-account-form__link _link">
                                <a href="#">Sign Up</a>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.gt-account {
	position: fixed;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
	z-index: 100;
	background-color: rgba(0, 0, 0, .25);
}
.gt-account__container {
	position: fixed;
	top: 50%;
	transform: translateY(-50%);
	width: 100%;
	max-height: 100%;
}
.login__container {
	position: relative;
	width: 500px;
	background-color: #F9F6F2;
	border-radius: 5px;
	padding: 60px 25px;
}
.login__title {
	text-align: center;
	font-size: 32px;
}
.gt-account-form {
	width: 100%;
}
.gt-account-form__input {
	width: 100%;
}
.input__container {
	padding: 15px;
}
.gt-account-form__btn {
	width: 100%;
	padding: 15px;
}
.login__btn {
	color: white;
	width: 100%;
	border-radius: 5px;
	font-size: 18px;
	padding: 15px;
	background-color: #3a3a3a;
	transition: all .25s;
}
.login__btn:hover {
	background-color: #141518;
}
.gt-account-form__support {
	padding: 0 15px;
	width: 100%;
	display: flex;
	justify-content: space-between;
}
.gt-account-form__link {
	font-size: 14px;
	width: fit-content;
}
.gt-account-form__link::after {
	background-color: #3a3a3a;
}
.close-icon {
	position: absolute;
	top: 5px;
	right: 5px;
	width: 16px;
	height: 16px;
	margin: 16px;
	cursor: pointer;
}
</style>

<script>
export default {
    
}
</script>
