document.addEventListener("DOMContentLoaded", () => {

    const btnRegister = document.getElementById("btnRegister");

    if (!btnRegister) {
        console.error("❌ No se encontró el botón #btnRegister");
        return;
    }

    btnRegister.addEventListener("click", async () => {

        const nombre = document.getElementById("nombre").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();
        const rol = document.getElementById("rol").value.trim();

        if (!nombre || !email || !password || !rol) {
            alert("Campos incompletos");
            return;
        }

        const data = {
            nombre: nombre,
            email: email,
            contraseña: password,
            rol: rol,
        };

        try {
            const response = await fetch("/api/registrar/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.success) {
                alert("Cuenta creada con éxito 🎉");
                window.location.href = "/login/";
            } else {
                alert(result.msg || "Error en el registro.");
            }

        } catch (error) {
            console.error("Error:", error);
            alert("Error en el servidor");
        }
    });
});

