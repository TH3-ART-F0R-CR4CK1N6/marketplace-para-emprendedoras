// Cerrar alertas
document.querySelectorAll('.close-alert').forEach(button => {
    button.addEventListener('click', function() {
        this.parentElement.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            this.parentElement.remove();
        }, 300);
    });
});

// Auto-cerrar alertas después de 5 segundos
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, 5000);
});

// Animación de slideOut
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Prevenir envío múltiple de formularios
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.6';
            submitBtn.textContent = 'Procesando...';
            
            // Re-habilitar después de 3 segundos por si hay error
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
            }, 3000);
        }
    });
});
