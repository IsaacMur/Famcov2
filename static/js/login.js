document.addEventListener("DOMContentLoaded", function () {
   
    // Verificar si los campos están vacíos
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (username === "" || password === "") {
            Swal.fire({
                icon: 'warning',
                title: 'Campos vacíos',
                text: 'Por favor, ingresa usuario y contraseña para entrar.',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true
            });
            return;
        }

        // Verificador de credenciales
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        fetch("/login", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/administrador";
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Credenciales Incorrectas',
                        text: data.message,
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true
                    });
                }
            })
            .catch(error => console.error("Error en la solicitud:", error));
    });

    // Funcion del ojo para ver contraseña
    window.onload = function () {
        const toggleIcon = document.getElementById('togglePasswordIcon');
        toggleIcon.classList.add('fa-eye-slash');
    };
    
    window.togglePasswordVisibility = function () {
        const passwordField = document.getElementById('password');
        const toggleIcon = document.getElementById('togglePasswordIcon');
    
        if (passwordField.type === 'password') {
            // Cambiar a texto y mostrar ícono de ojo abierto
            passwordField.type = 'text';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        } else {
            // Cambiar a contraseña y mostrar ícono de ojo cerrado
            passwordField.type = 'password';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        }
    };
});
