console.log("Login JS cargado correctamente");

document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const emailValue = document.getElementById("email").value.trim();
    const passwordValue = document.getElementById("password").value.trim();

    console.log("Email enviado:", emailValue);
    console.log("Password enviado:", passwordValue);

    if (!emailValue || !passwordValue) {
        alert("Completa todos los campos");
        return;
    }

    const response = await fetch("/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: JSON.stringify({
            usuario: emailValue,   // 👈 EXACTO como lo pide la vista
            password: passwordValue
        })
    });

    const data = await response.json();

    console.log("Respuesta del backend:", data);

    if (data.success) {
        alert("Bienvenido " + data.usuario);
        window.location.href = "/dashboard/";
    } else {
        alert(data.msg);
    }
});


