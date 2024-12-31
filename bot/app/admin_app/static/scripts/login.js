const btnSub = document.getElementById("btn-login");
const login = document.getElementById('username');
const password = document.getElementById('password')

const checkEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

const checkPhone = (phone) => {
    const phoneRegex = /^\+7\d{10}$/;
    return phoneRegex.test(phone);
}

const checkLogin = () => {

}