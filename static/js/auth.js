// function togglePassword() {
//             const passwordInput = document.getElementById('password');
//             const eyeIcon = document.getElementById('eyeIcon');
            
//             if (passwordInput.type === 'password') {
//                 passwordInput.type = 'text';
//                 eyeIcon.classList.remove('fa-eye');
//                 eyeIcon.classList.add('fa-eye-slash');
//             } else {
//                 passwordInput.type = 'password';
//                 eyeIcon.classList.remove('fa-eye-slash');
//                 eyeIcon.classList.add('fa-eye');
//             }
//         }

        // const loginForm = document.getElementById('loginForm');
        // loginForm.addEventListener('submit', (e) => {
        //     e.preventDefault();
            
        //     const email = document.getElementById('email').value;
        //     const password = document.getElementById('password').value;

        //     // For demo purposes - show error
        //     if (email && password) {
        //         // Simulate login - in real app, this would be an API call
        //         if (password === 'demo') {
        //             alert('Login successful! Redirecting to dashboard...');
        //             // window.location.href = 'dashboard.html';
        //         } else {
        //             showError('Invalid email or password. Try password: "demo"');
        //         }
        //     } else {
        //         showError('Please fill in all fields');
        //     }
        // });

        // 
        


        function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}
 
document.addEventListener("DOMContentLoaded", function () {
    const errorBox = document.getElementById("errorBox");

    if (errorBox) {
        setTimeout(() => {
            errorBox.style.opacity = "0";
            errorBox.style.transition = "opacity 0.5s ease";

            setTimeout(() => {
                errorBox.remove();
            }, 500);
        }, 4000); // disappears after 4 seconds
    }
});
