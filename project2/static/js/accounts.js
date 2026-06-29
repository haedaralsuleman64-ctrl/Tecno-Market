// تبديل إظهار/إخفاء كلمة المرور
function initializePasswordToggles() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            if (!passwordInput) return;
            
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // تغيير الأيقونة
            const icon = this.querySelector('i');
            if (icon) {
                if (type === 'text') {
                    icon.classList.remove('bi-eye');
                    icon.classList.add('bi-eye-slash');
                } else {
                    icon.classList.remove('bi-eye-slash');
                    icon.classList.add('bi-eye');
                }
            }
        });
    });
}

// تبديل الوضع الليلي/النهاري
function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeText = document.querySelector('.theme-text');
    
    if (!themeToggle) return;
    
    // التحقق من التفضيل المحفوظ
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    if (themeText) {
        updateThemeText(savedTheme, themeText);
    }

    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        if (themeText) {
            updateThemeText(newTheme, themeText);
        }
    });
}

function updateThemeText(theme, themeTextElement) {
    themeTextElement.textContent = theme === 'light' ? 'الوضع النهاري' : 'الوضع الليلي';
}

// تأثيرات عند التركيز على الحقول
function initializeFormEffects() {
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// التحقق من صحة النماذج
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                // إظهار رسالة الخطأ
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger';
                errorDiv.innerHTML = '<i class="bi bi-exclamation-triangle"></i> يرجى ملء جميع الحقول المطلوبة';
                this.prepend(errorDiv);
                
                // إخفاء الرسالة بعد 5 ثواني
                setTimeout(() => {
                    errorDiv.remove();
                }, 5000);
            }
        });
    });
}

// تأثيرات hover للوسائط الاجتماعية
function initializeSocialButtons() {
    const socialButtons = document.querySelectorAll('.btn-social');
    socialButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.15)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
        });
    });
}

// تأثيرات الصفحة
function initializeProfileEffects() {
    // تأثيرات ظهور العناصر
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // مراقبة العناصر
    document.querySelectorAll('.info-card, .stat-card').forEach(card => {
        observer.observe(card);
    });
}

// تهيئة التأثيرات عند تحميل الصفحة
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeProfileEffects);
} else {
    initializeProfileEffects();
}

// تهيئة جميع الوظائف
function initializeAll() {
    initializePasswordToggles();
    initializeThemeToggle();
    initializeFormEffects();
    initializeFormValidation();
    initializeSocialButtons();
}

// تحميل الكود عند اكتمال DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAll);
} else {
    initializeAll();
}