document.addEventListener("DOMContentLoaded", function () {

    const btnRegister = document.getElementById("btnRegister");

    if (!btnRegister) {
        console.error("❌ No se encontró el botón #btnRegister");
        return;
    }

    btnRegister.addEventListener("click", async function (e) {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!nombre || !email || !password) {
            alert("Completa todos los campos.");
            return;
        }

        const data = {
            nombre: nombre,
            email: email,
            contraseña: password
        };

        try {
            const response = await fetch("/api/registrar/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log(result);

            if (result.success) {
                alert("Cuenta creada correctamente ✨");

                // guardar sesión directa si quieres
                sessionStorage.setItem("usuario", result.rol);
                sessionStorage.setItem("email", email);

                window.location.href = "/login/";

            } else {
                alert(result.msg);
            }

        } catch (error) {
            console.error("Error en registro:", error);
            alert("Error al registrar usuario");
        }
    });
});
