// ملف JavaScript الرئيسي لموقع مؤسسة ركائز

// التحكم في اللغات والترجمة
const translations = {
    ar: {
        home: "الرئيسية",
        about: "من نحن",
        services: "خدماتنا",
        news: "الأخبار",
        team: "فريق العمل",
        contact: "اتصل بنا",
        welcomeTitle: "مرحباً بكم في مؤسسة ركائز",
        welcomeDesc: "نهدف إلى تقديم أفضل الخدمات المجتمعية والتنموية",
        learnMore: "اعرف المزيد",
        ourServices: "خدماتنا",
        servicesDesc: "نقدم مجموعة متنوعة من الخدمات المجتمعية والتنموية",
        ourTeam: "فريق العمل",
        teamDesc: "تعرف على الفريق المتميز الذي يعمل على تحقيق رسالتنا",
        contactUs: "تواصل معنا",
        contactDesc: "نحن هنا للإجابة على استفساراتكم ومساعدتكم",
        name: "الاسم",
        email: "البريد الإلكتروني",
        phone: "رقم الهاتف",
        message: "الرسالة",
        subject: "الموضوع",
        send: "إرسال",
        loading: "جاري التحميل...",
        success: "تم الإرسال بنجاح!",
        error: "حدث خطأ، يرجى المحاولة مرة أخرى"
    },
    en: {
        home: "Home",
        about: "About Us",
        services: "Our Services",
        news: "News",
        team: "Our Team",
        contact: "Contact Us",
        welcomeTitle: "Welcome to Rakaiz Foundation",
        welcomeDesc: "We aim to provide the best community and development services",
        learnMore: "Learn More",
        ourServices: "Our Services",
        servicesDesc: "We provide a variety of community and development services",
        ourTeam: "Our Team",
        teamDesc: "Meet our distinguished team working to achieve our mission",
        contactUs: "Contact Us",
        contactDesc: "We are here to answer your questions and help you",
        name: "Name",
        email: "Email",
        phone: "Phone",
        message: "Message",
        subject: "Subject",
        send: "Send",
        loading: "Loading...",
        success: "Message sent successfully!",
        error: "An error occurred, please try again"
    },
    tr: {
        home: "Ana Sayfa",
        about: "Hakkımızda",
        services: "Hizmetlerimiz",
        news: "Haberler",
        team: "Ekibimiz",
        contact: "İletişim",
        welcomeTitle: "Rakaiz Vakfına Hoş Geldiniz",
        welcomeDesc: "En iyi toplumsal ve kalkınma hizmetlerini sunmayı hedefliyoruz",
        learnMore: "Daha Fazla Bilgi",
        ourServices: "Hizmetlerimiz",
        servicesDesc: "Çeşitli toplumsal ve kalkınma hizmetleri sunuyoruz",
        ourTeam: "Ekibimiz",
        teamDesc: "Misyonumuzu gerçekleştirmek için çalışan seçkin ekibimizi tanıyın",
        contactUs: "İletişim",
        contactDesc: "Sorularınızı yanıtlamak ve size yardımcı olmak için buradayız",
        name: "İsim",
        email: "E-posta",
        phone: "Telefon",
        message: "Mesaj",
        subject: "Konu",
        send: "Gönder",
        loading: "Yükleniyor...",
        success: "Mesaj başarıyla gönderildi!",
        error: "Bir hata oluştu, lütfen tekrar deneyin"
    }
};

// المتغيرات العامة
let currentLang = 'ar';

// تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

// تهيئة الموقع
function initializeWebsite() {
    setupMobileMenu();
    setupLanguageSwitcher();
    setupAnimations();
    setupForms();
    setupSmoothScrolling();
    loadLanguage(getCurrentLanguage());
}

// إعداد القائمة المحمولة
function setupMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // إغلاق القائمة عند النقر على رابط
        document.querySelectorAll('.nav-item a').forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}

// إعداد تبديل اللغات
function setupLanguageSwitcher() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            switchLanguage(lang);
        });
    });
}

// تبديل اللغة
function switchLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('selectedLanguage', lang);
    loadLanguage(lang);
    updateLanguageButtons(lang);
    updatePageDirection(lang);
}

// تحميل اللغة
function loadLanguage(lang) {
    const elements = document.querySelectorAll('[data-translate]');
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });
}

// تحديث أزرار اللغة
function updateLanguageButtons(lang) {
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
        }
    });
}

// تحديث اتجاه الصفحة
function updatePageDirection(lang) {
    const body = document.body;
    if (lang === 'ar') {
        body.setAttribute('dir', 'rtl');
        body.classList.remove('ltr');
        body.classList.add('rtl');
    } else {
        body.setAttribute('dir', 'ltr');
        body.classList.remove('rtl');
        body.classList.add('ltr');
    }
}

// الحصول على اللغة الحالية
function getCurrentLanguage() {
    return localStorage.getItem('selectedLanguage') || 'ar';
}

// إعداد الحركات والانيميشن
function setupAnimations() {
    // Intersection Observer للعناصر المتحركة
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // إضافة المراقب لجميع العناصر التي تحتاج انيميشن
    document.querySelectorAll('.fade-in').forEach(element => {
        observer.observe(element);
    });

    // إضافة فئة fade-in للعناصر التي تحتاج انيميشن
    document.querySelectorAll('.service-card, .team-member, .section-title').forEach(element => {
        element.classList.add('fade-in');
        observer.observe(element);
    });
}

// إعداد النماذج
function setupForms() {
    const contactForm = document.getElementById('contactForm');
    const serviceForm = document.getElementById('serviceForm');
    const appointmentForm = document.getElementById('appointmentForm');

    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }

    if (serviceForm) {
        serviceForm.addEventListener('submit', handleServiceSubmit);
    }

    if (appointmentForm) {
        appointmentForm.addEventListener('submit', handleAppointmentSubmit);
    }
}

// معالجة نموذج التواصل
async function handleContactSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    try {
        // تعطيل الزر وإظهار التحميل
        submitBtn.disabled = true;
        submitBtn.textContent = translations[currentLang].loading;

        // محاكاة إرسال البيانات
        await simulateFormSubmission(formData);

        // إظهار رسالة النجاح
        showNotification(translations[currentLang].success, 'success');
        form.reset();

    } catch (error) {
        console.error('Error:', error);
        showNotification(translations[currentLang].error, 'error');
    } finally {
        // إعادة تفعيل الزر
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// معالجة نموذج طلب الخدمة
async function handleServiceSubmit(e) {
    e.preventDefault();
    await handleFormSubmit(e, 'service');
}

// معالجة نموذج حجز الموعد
async function handleAppointmentSubmit(e) {
    e.preventDefault();
    await handleFormSubmit(e, 'appointment');
}

// معالجة عامة للنماذج
async function handleFormSubmit(e, type) {
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    try {
        submitBtn.disabled = true;
        submitBtn.textContent = translations[currentLang].loading;

        await simulateFormSubmission(formData, type);

        showNotification(translations[currentLang].success, 'success');
        form.reset();

    } catch (error) {
        console.error('Error:', error);
        showNotification(translations[currentLang].error, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// محاكاة إرسال النموذج
function simulateFormSubmission(formData, type = 'contact') {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // هنا يمكنك إضافة منطق إرسال البيانات الفعلي
            // مثل fetch إلى API الخاص بك
            const success = Math.random() > 0.1; // محاكاة نجاح 90%
            
            if (success) {
                resolve({
                    message: 'Form submitted successfully',
                    type: type,
                    data: Object.fromEntries(formData)
                });
            } else {
                reject(new Error('Submission failed'));
            }
        }, 2000);
    });
}

// إظهار الإشعارات
function showNotification(message, type = 'info') {
    // إنشاء عنصر الإشعار
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">
                ${type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ'}
            </span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    // إضافة الأنماط إذا لم تكن موجودة
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                max-width: 400px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 10000;
                animation: slideInRight 0.3s ease-out;
            }
            .notification-success {
                border-left: 4px solid #4CAF50;
            }
            .notification-error {
                border-left: 4px solid #f44336;
            }
            .notification-info {
                border-left: 4px solid #2196F3;
            }
            .notification-content {
                display: flex;
                align-items: center;
                padding: 15px;
            }
            .notification-icon {
                margin-left: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            .notification-success .notification-icon {
                color: #4CAF50;
            }
            .notification-error .notification-icon {
                color: #f44336;
            }
            .notification-info .notification-icon {
                color: #2196F3;
            }
            .notification-message {
                flex: 1;
                margin: 0 10px;
            }
            .notification-close {
                background: none;
                border: none;
                font-size: 20px;
                cursor: pointer;
                color: #999;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .notification-close:hover {
                color: #333;
            }
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    // إضافة الإشعار إلى الصفحة
    document.body.appendChild(notification);

    // إزالة الإشعار تلقائياً بعد 5 ثواني
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// إعداد التمرير السلس
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// إعداد الخريطة (Google Maps)
function initMap() {
    // إحداثيات مؤسسة ركائز (يجب تعديلها حسب الموقع الفعلي)
    const location = { lat: 41.0082, lng: 28.9784 }; // إسطنبول كمثال
    
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: location,
        styles: [
            {
                featureType: 'all',
                elementType: 'geometry.fill',
                stylers: [{ color: '#fce4ec' }]
            },
            {
                featureType: 'water',
                elementType: 'geometry.fill',
                stylers: [{ color: '#e91e63' }]
            }
        ]
    });

    const marker = new google.maps.Marker({
        position: location,
        map: map,
        title: 'مؤسسة ركائز',
        icon: {
            url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="#e91e63">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
            `),
            scaledSize: new google.maps.Size(40, 40)
        }
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="text-align: center; font-family: 'Cairo', sans-serif;">
                <h4 style="color: #e91e63; margin: 0;">مؤسسة ركائز</h4>
                <p style="margin: 5px 0;">نحن هنا لخدمتكم</p>
            </div>
        `
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });
}

// دوال إضافية للإدارة
class AdminManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupAdminAuth();
        this.setupContentManagement();
    }

    setupAdminAuth() {
        const loginForm = document.getElementById('adminLoginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', this.handleLogin.bind(this));
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const username = formData.get('username');
        const password = formData.get('password');

        try {
            // هنا يجب إضافة التحقق الفعلي من بيانات الدخول
            const isValid = await this.validateCredentials(username, password);
            
            if (isValid) {
                localStorage.setItem('adminLoggedIn', 'true');
                window.location.href = 'admin-dashboard.html';
            } else {
                showNotification('بيانات الدخول غير صحيحة', 'error');
            }
        } catch (error) {
            showNotification('حدث خطأ في تسجيل الدخول', 'error');
        }
    }

    async validateCredentials(username, password) {
        // محاكاة التحقق من بيانات الدخول
        return new Promise((resolve) => {
            setTimeout(() => {
                // يجب استبدال هذا بالتحقق الفعلي من قاعدة البيانات
                resolve(username === 'admin' && password === 'admin123');
            }, 1000);
        });
    }

    setupContentManagement() {
        this.setupNewsManagement();
        this.setupServicesManagement();
        this.setupTeamManagement();
    }

    setupNewsManagement() {
        const addNewsBtn = document.getElementById('addNewsBtn');
        if (addNewsBtn) {
            addNewsBtn.addEventListener('click', this.showAddNewsModal.bind(this));
        }
    }

    setupServicesManagement() {
        const addServiceBtn = document.getElementById('addServiceBtn');
        if (addServiceBtn) {
            addServiceBtn.addEventListener('click', this.showAddServiceModal.bind(this));
        }
    }

    setupTeamManagement() {
        const addMemberBtn = document.getElementById('addMemberBtn');
        if (addMemberBtn) {
            addMemberBtn.addEventListener('click', this.showAddMemberModal.bind(this));
        }
    }

    showAddNewsModal() {
        // إنشاء نموذج إضافة الأخبار
        const modal = this.createModal('إضافة خبر جديد', `
            <form id="addNewsForm">
                <div class="form-group">
                    <label>عنوان الخبر</label>
                    <input type="text" name="title" required>
                </div>
                <div class="form-group">
                    <label>محتوى الخبر</label>
                    <textarea name="content" rows="5" required></textarea>
                </div>
                <div class="form-group">
                    <label>صورة الخبر</label>
                    <input type="file" name="image" accept="image/*">
                </div>
                <div class="form-group">
                    <label>تاريخ النشر</label>
                    <input type="date" name="date" required>
                </div>
                <button type="submit" class="btn btn-primary">إضافة الخبر</button>
            </form>
        `);

        document.getElementById('addNewsForm').addEventListener('submit', this.handleAddNews.bind(this));
    }

    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;

        // إضافة أنماط المودال إذا لم تكن موجودة
        if (!document.querySelector('#modal-styles')) {
            const styles = document.createElement('style');
            styles.id = 'modal-styles';
            styles.textContent = `
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                }
                .modal-content {
                    background: white;
                    border-radius: 10px;
                    max-width: 500px;
                    width: 90%;
                    max-height: 80%;
                    overflow-y: auto;
                }
                .modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px;
                    border-bottom: 1px solid #eee;
                }
                .modal-header h3 {
                    margin: 0;
                    color: var(--primary-color);
                }
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: #999;
                }
                .modal-body {
                    padding: 20px;
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(modal);
        return modal;
    }

    async handleAddNews(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            // محاكاة إضافة الخبر
            await this.simulateAddNews(formData);
            showNotification('تم إضافة الخبر بنجاح', 'success');
            e.target.closest('.modal-overlay').remove();
            // إعادة تحميل قائمة الأخبار
            this.refreshNewsList();
        } catch (error) {
            showNotification('حدث خطأ في إضافة الخبر', 'error');
        }
    }

    simulateAddNews(formData) {
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('News added:', Object.fromEntries(formData));
                resolve();
            }, 1000);
        });
    }

    refreshNewsList() {
        // إعادة تحميل قائمة الأخبار من قاعدة البيانات
        console.log('Refreshing news list...');
    }
}

// تهيئة مدير الإدارة
const adminManager = new AdminManager();

// دوال مساعدة
function formatDate(date) {
    return new Date(date).toLocaleDateString(currentLang === 'ar' ? 'ar-SA' : currentLang === 'tr' ? 'tr-TR' : 'en-US');
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[0-9\s\-\(\)]{10,}$/;
    return re.test(phone);
}

// التحقق من حالة تسجيل الدخول للإدارة
function checkAdminAuth() {
    const isLoggedIn = localStorage.getItem('adminLoggedIn') === 'true';
    const adminPages = ['admin-dashboard.html', 'admin-news.html', 'admin-services.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (adminPages.includes(currentPage) && !isLoggedIn) {
        window.location.href = 'admin-login.html';
    }
}

// تسجيل الخروج من الإدارة
function adminLogout() {
    localStorage.removeItem('adminLoggedIn');
    window.location.href = 'admin-login.html';
}

// تشغيل التحقق من الإدارة عند تحميل الصفحة
checkAdminAuth();