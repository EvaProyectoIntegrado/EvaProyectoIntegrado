console.log("Login JS cargado correctamente");

document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const emailValue = document.getElementById("email").value.trim();
    const passwordValue = document.getElementById("password").value.trim();

    if (!emailValue || !passwordValue) {
        alert("Completa todos los campos");
        return;
    }

    const response = await fetch("/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: emailValue,
            password: passwordValue
        })
    });

    const data = await response.json();

    if (data.success) {
        // guardar token y rol en sessionStorage
        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("rol", data.rol);

        alert("Bienvenida " + data.usuario);
        window.location.href = "/dashboard/";
    } else {
        alert(data.msg);
    }
});



