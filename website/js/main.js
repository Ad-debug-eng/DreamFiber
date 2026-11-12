// Main JavaScript file for DreamC ISP
document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileBtn) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('mobile-active');
            document.body.classList.toggle('menu-open');
        });
    }

    // Sticky Header & Hide on scroll down
    const header = document.getElementById('navbar');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        // Sticky blur effect
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        // Hide/Show effect
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
            // Scrolling down - ONLY hide if the mobile menu is NOT open
            if (!navLinks.classList.contains('mobile-active')) {
                header.classList.add('header-hidden');
            }
        } else {
            // Scrolling up
            header.classList.remove('header-hidden');
        }
        lastScrollY = window.scrollY;
    });

    // ... Keep your Pricing Logic below ...
// Existing code ends here
});
/* ------------------- Pricing Logic for Homepage ------------------- */
const wifiPlans = [
    { speed: '50 Mbps', prices: {1: 499, 3: 1300, 6: 2500, 12: 5000}, best: false },
    { speed: '100 Mbps', prices: {1: 699, 3: 1700, 6: 3500, 12: 6200}, best: false },
    { speed: '200 Mbps', prices: {1: 899, 3: 2300, 6: 5000, 12: 9000}, best: true },
    { speed: '300 Mbps', prices: {1: 1300, 3: 3500, 6: 7000, 12: 13000}, best: false },
];
const ottPlans = [
    {
        speed: '50 Mbps',
        otts: ['JioHotstar','Zee5','SonyLIV','+10 OTTs'],
        channels: '800+ Live TV Channels',
        prices: {3:1797,6:3299,12:5999},
        best: false
    },
    {
        speed: '100 Mbps',
        otts: ['JioHotstar','Zee5','SonyLIV','+10 OTTs'],
        channels: '800+ Live TV Channels',
        prices: {3:2397,6:4499,12:8399},
        best: true
    },
    {
        speed: '200 Mbps',
        otts: ['JioHotstar','Zee5','SonyLIV','+10 OTTs'],
        channels: '800+ Live TV Channels',
        prices: {3:2997,6:5699,12:10799},
        best: false
    },
    {
        speed: '300 Mbps',
        otts: ['JioHotstar','Amazon Prime','Zee5','SonyLIV','+10 OTTs'],
        channels: '800+ Live TV Channels',
        prices: {3:3897,6:7494,12:14388},
        best: false
    },
];
function renderWifiHome(dur) {
    const container = document.getElementById('home-wifi-cards');
    if (!container) return;
    container.innerHTML = '';
    wifiPlans.forEach(plan => {
        const total = plan.prices[dur];
        const perMonth = total / dur;
        const perMonthText = Number.isInteger(perMonth)
            ? perMonth.toLocaleString('en-IN')
            : perMonth.toLocaleString('en-IN', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
        const card = document.createElement('div');
        card.className = 'pricing-card' + (plan.best ? ' best' : '');
        card.innerHTML = `
            ${plan.best ? '<div class="best-badge">BEST SELLER</div>' : ''}
            <div class="plan-speed">${plan.speed}</div>
            <div class="plan-type">Unlimited Fiber</div>
            <div class="price-per-month"><sup>₹</sup>${perMonthText}</div>
            <div class="price-per-month-label">per month</div>
            ${dur > 1 ? `<div class="monthly-highlight">₹${perMonthText}/month</div>` : ''}
            ${dur > 1 ? `<span class="price-total">Total: ₹${total.toLocaleString('en-IN')} for ${dur} months</span>` : '<span class="price-total">&nbsp;</span>'}
            <ul class="plan-features">
                <li><ion-icon name="checkmark-circle"></ion-icon>Unlimited Data</li>
                <li><ion-icon name="checkmark-circle"></ion-icon>Free Dual-Band Router</li>
                <li><ion-icon name="checkmark-circle"></ion-icon>Free Installation</li>
            </ul>
            <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I+am+interested+in+the+${plan.speed}+Unlimited+Fiber+plan.+Please+check+feasibility+for+my+area." target="_blank" class="btn-whatsapp-cta">
                <ion-icon name="logo-whatsapp"></ion-icon> Check Availability
            </a>
        `;
        container.appendChild(card);
    });
}
function renderOttHome(dur) {
    const container = document.getElementById('home-ott-cards');
    if (!container) return;
    container.innerHTML = '';
    ottPlans.forEach(plan => {
        const total = plan.prices[dur];
        const perMonth = total / dur;
        const perMonthText = Number.isInteger(perMonth)
            ? perMonth.toLocaleString('en-IN')
            : perMonth.toLocaleString('en-IN', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
        const card = document.createElement('div');
        card.className = 'pricing-card' + (plan.best ? ' best' : '');
        const ottHtml = plan.otts.map(o => `<span class="ott-logo">${o}</span>`).join('');
        card.innerHTML = `
            ${plan.best ? '<div class="best-badge">BEST SELLER</div>' : ''}
            <div class="plan-speed">${plan.speed}</div>
            <div class="plan-type">Fiber + OTT + Live TV</div>
            <div class="ott-logos">${ottHtml}</div>
            <div class="price-per-month"><sup>₹</sup>${perMonthText}</div>
            <div class="price-per-month-label">per month</div>
            ${dur > 1 ? `<div class="monthly-highlight">₹${perMonthText}/month</div>` : ''}
            <span class="price-total">Total: ₹${total.toLocaleString('en-IN')} for ${dur} months</span>
            <ul class="plan-features">
                <li><ion-icon name="checkmark-circle"></ion-icon>Unlimited Data</li>
                <li><ion-icon name="checkmark-circle"></ion-icon>${plan.channels}</li>
                <li><ion-icon name="checkmark-circle"></ion-icon>Free Installation</li>
            </ul>
            <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I+am+interested+in+the+${plan.speed}+Fiber+%2B+OTT+bundle.+Please+check+feasibility+for+my+area." target="_blank" class="btn-whatsapp-cta">
                <ion-icon name="logo-whatsapp"></ion-icon> Check Availability
            </a>
        `;
        container.appendChild(card);
    });
}
let activeHomeWifiDur = 1;
let activeHomeOttDur = 3;
function setupHomeDurButtons(sectionId, renderFn, getDur, setDur) {
    const section = document.getElementById(sectionId);
    if (!section) return;
    section.querySelectorAll('.dur-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            section.querySelectorAll('.dur-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            setDur(parseInt(btn.dataset.dur));
            renderFn(parseInt(btn.dataset.dur));
        });
    });
}
renderWifiHome(activeHomeWifiDur);
renderOttHome(activeHomeOttDur);
setupHomeDurButtons('tab-wifi', renderWifiHome, () => activeHomeWifiDur, v => activeHomeWifiDur = v);
setupHomeDurButtons('tab-ott', renderOttHome, () => activeHomeOttDur, v => activeHomeOttDur = v);

window.toggleOtt = function(btn) {
    // Navigate up to the grid container, then get its next sibling (the dropdown)
    const dropdown = btn.parentElement.nextElementSibling;
    if (dropdown.classList.contains('active')) {
        dropdown.classList.remove('active');
        btn.textContent = btn.dataset.originalText || '+17';
    } else {
        if (!btn.dataset.originalText) {
            btn.dataset.originalText = btn.textContent;
        }
        dropdown.classList.add('active');
        btn.textContent = '-';
    }
}

/* ------------------- Cloudflare Worker Telegram Form Logic ------------------- */

// Function to send data to Cloudflare Worker
async function sendToTelegram(messageText, buttonElement) {
    // ---------------------------------------------------------
    // ENTER YOUR CLOUDFLARE WORKER URL HERE:
    const workerURL = "https://dreamcables-form.adwait001ahirekar.workers.dev"; 
    // ---------------------------------------------------------
    
    const originalText = buttonElement.innerText;
    buttonElement.innerText = "Sending...";
    buttonElement.disabled = true;

    try {
        const response = await fetch(workerURL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: messageText }) 
        });

        if (response.ok) {
            alert("Message Sent Successfully!");
            document.querySelectorAll('form').forEach(f => f.reset());
        } else {
            alert("Failed to send. Please check your connection or contact us via WhatsApp.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Network error occurred.");
    } finally {
        buttonElement.innerText = originalText;
        buttonElement.disabled = false;
    }
}

// Attach Form Listeners securely inside DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // 1. Enterprise Form Listener
    const enterpriseForm = document.getElementById('enterpriseForm');
    if (enterpriseForm) {
        enterpriseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('entName').value;
            const phone = document.getElementById('entPhone').value;
            const email = document.getElementById('entEmail').value || 'Not provided';
            const address = document.getElementById('entAddress').value || 'Not provided';
            const reqs = document.getElementById('entReq').value;

            const tgMessage = `🏢 *New Enterprise Inquiry*\n\n` +
                              `*Name/Company:* ${name}\n` +
                              `*Phone:* ${phone}\n` +
                              `*Email:* ${email}\n` +
                              `*Address:* ${address}\n` +
                              `*Requirements:* ${reqs}`;

            const btn = enterpriseForm.querySelector('button[type="submit"]');
            sendToTelegram(tgMessage, btn);
        });
    }

    // 2. Contact Form Listener
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const code = document.getElementById('countryCode') ? document.getElementById('countryCode').value : "";
            const phoneInput = document.getElementById('phone').value;
            const phone = code + phoneInput;
            const email = document.getElementById('email').value || 'Not provided';
            const service = document.getElementById('service').value;
            const msg = document.getElementById('message').value;

            const tgMessage = `👤 *New Contact Form*\n\n` +
                              `*Name:* ${name}\n` +
                              `*Phone:* ${phone}\n` +
                              `*Email:* ${email}\n` +
                              `*Service:* ${service}\n` +
                              `*Message:* ${msg}`;

            const btn = contactForm.querySelector('button[type="submit"]');
            sendToTelegram(tgMessage, btn);
        });
    }
});