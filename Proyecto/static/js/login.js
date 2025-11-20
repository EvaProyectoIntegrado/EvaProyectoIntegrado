document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("btnLogin");
    const emailInput = document.getElementById("email");
    const passInput = document.getElementById("password");

    if (!btn) {
        console.error("btnLogin no existe en el DOM");
        return;
    }

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const email = emailInput.value.trim();
        const password = passInput.value.trim();

        if (!email || !password) {
            alert("Completa todos los campos.");
            return;
        }

        const data = {
            email: email,
            contraseña: password
        };

        try {
            const response = await fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                sessionStorage.setItem("usuario", result.rol);
                window.location.href = "/dashboard/";
            } else {
                alert(result.msg);
            }

        } catch (error) {
            console.error("Error:", error);
            alert("Error de conexión con el servidor.");
        }
    });
});
