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

const EmailOrPhone = () => {
    const input = login.value.trim();
    return input.includes('@');
}

const fetchAuth = async (username, password) => {
    const payload = new URLSearchParams({
            username: username,
            password: password
        });

        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: payload,
        };

        try{
            const response = await fetch("/api/auth/token", requestOptions);
            if (response.ok){
                const data = await response.json()
                localStorage.setItem("token", data.access_token)
                location.replace("/")
            }
        } catch (e){
            throw new Error(e)
        }

}

const handleLogin = async () => {
    if (EmailOrPhone === true) {
        if (checkEmail(login)) {

        } else {
            alert("E-mail введен некорректно!");
            return;
        }
    } else {
        if (checkPhone(login)) {
            // post
        } else {
            alert("Номер телефона введен некорректно! Номер должен выглядеть: +79XXXXXXXXXX");
            return;
        }
    }
}