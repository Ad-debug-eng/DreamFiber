/* -------------------------------------------------------------
   DreamFiber Telegram Form Integration
   Connected via Cloudflare Worker
   Endpoint: https://dreamcables-form.adwait001ahirekar.workers.dev
   ------------------------------------------------------------- */

const TELEGRAM_WORKER_URL = "https://dreamcables-form.adwait001ahirekar.workers.dev";

async function sendToTelegram(messageText, buttonElement, successMsg) {
    const originalText = buttonElement ? buttonElement.innerHTML : "";
    if (buttonElement) {
        buttonElement.innerText = "Sending...";
        buttonElement.disabled = true;
    }

    try {
        const response = await fetch(TELEGRAM_WORKER_URL, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json" 
            },
            body: JSON.stringify({ message: messageText })
        });

        if (response.ok) {
            alert(successMsg || "Thank you! Your message has been sent successfully. Our team will contact you shortly.");
            document.querySelectorAll('form').forEach(f => f.reset());
            // If inside a modal, close modal if bootstrap is available
            const openModal = document.querySelector('.modal.show');
            if (openModal && window.bootstrap && window.bootstrap.Modal) {
                const modalInstance = bootstrap.Modal.getInstance(openModal);
                if (modalInstance) modalInstance.hide();
            }
        } else {
            alert("Failed to send message. Please reach out to us directly on WhatsApp or Call.");
        }
    } catch (error) {
        console.error("Form Telegram submission error:", error);
        alert("A network error occurred. Please contact us directly via WhatsApp (+91 9272162704) or Call.");
    } finally {
        if (buttonElement) {
            buttonElement.innerHTML = originalText;
            buttonElement.disabled = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 1. Get in Touch Form (contact.html)
    const contactForm = document.getElementById('contactForm');
    const contactPhone = document.getElementById('contactPhone');
    const phoneWrap = document.getElementById('contactPhoneWrap');
    const phoneError = document.getElementById('phoneError');

    if (contactPhone) {
        contactPhone.addEventListener('input', function() {
            let val = this.value.replace(/\D/g, '');
            // Smart strip country code or leading zero if pasted
            if (val.length === 12 && val.startsWith('91')) {
                val = val.substring(2);
            } else if (val.length === 11 && val.startsWith('0')) {
                val = val.substring(1);
            }
            this.value = val.slice(0, 10);

            if (this.value.length === 10) {
                if (phoneError) phoneError.style.display = 'none';
                if (phoneWrap) phoneWrap.classList.remove('has-error');
            }
        });

        contactPhone.addEventListener('blur', function() {
            if (this.value && this.value.length !== 10) {
                if (phoneError) {
                    phoneError.innerText = "Please enter a valid 10-digit mobile number.";
                    phoneError.style.display = 'block';
                }
                if (phoneWrap) phoneWrap.classList.add('has-error');
            }
        });
    }

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const nameInput = document.getElementById('contactName');
            const name = nameInput ? nameInput.value.trim() : '';

            // Mandatory 10-digit phone validation
            const phoneDigits = contactPhone ? contactPhone.value.replace(/\D/g, '') : '';
            if (phoneDigits.length !== 10) {
                if (phoneError) {
                    phoneError.innerText = "Please enter a valid 10-digit mobile number.";
                    phoneError.style.display = 'block';
                }
                if (phoneWrap) {
                    phoneWrap.classList.add('has-error');
                }
                if (contactPhone) {
                    contactPhone.focus();
                }
                return;
            } else {
                if (phoneError) phoneError.style.display = 'none';
                if (phoneWrap) phoneWrap.classList.remove('has-error');
            }

            const email = document.getElementById('contactEmail') ? (document.getElementById('contactEmail').value.trim() || 'Not provided') : 'Not provided';
            const serviceSelect = document.getElementById('contactService');
            const service = serviceSelect ? serviceSelect.value : '';
            if (!service) {
                alert("Please select an interested service.");
                if (serviceSelect) serviceSelect.focus();
                return;
            }

            const address = document.getElementById('contactAddress') ? (document.getElementById('contactAddress').value.trim() || 'Not provided') : 'Not provided';
            const messageInput = document.getElementById('contactMessage');
            const message = messageInput ? messageInput.value.trim() : '';

            if (!name) {
                alert("Please enter your full name.");
                if (nameInput) nameInput.focus();
                return;
            }

            if (!message) {
                alert("Please enter your message.");
                if (messageInput) messageInput.focus();
                return;
            }

            const headerTitle = service ? `Contact Us - ${service}` : 'Contact Us';
            const tgMessage = `*${headerTitle}*\n\n` +
                              `*Full Name:* ${name}\n` +
                              `*Contact Number:* +91 ${phoneDigits}\n` +
                              `*Email Address:* ${email}\n` +
                              `*Interested Service:* ${service}\n` +
                              `*Feasibility Address:* ${address}\n` +
                              `*Message:*\n${message}`;

            const btn = contactForm.querySelector('button[type="submit"]');
            sendToTelegram(tgMessage, btn, "Thank you, " + name + "! Your inquiry has been received. Our team will contact you shortly.");
        });
    }

    // 2. Leased Line Form (leased-line.html)
    const leasedLineForm = document.getElementById('leasedLineForm');
    if (leasedLineForm) {
        leasedLineForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const company = document.getElementById('illCompany') ? document.getElementById('illCompany').value.trim() : '';
            const person = document.getElementById('illPerson') ? document.getElementById('illPerson').value.trim() : '';
            const phone = document.getElementById('illPhone') ? document.getElementById('illPhone').value.trim() : '';
            const email = document.getElementById('illEmail') ? (document.getElementById('illEmail').value.trim() || 'Not provided') : 'Not provided';
            const bandwidth = document.getElementById('illBandwidth') ? document.getElementById('illBandwidth').value : '';
            const address = document.getElementById('illAddress') ? document.getElementById('illAddress').value.trim() : '';

            const tgMessage = `*Leased Line Request*\n\n` +
                              `*Company:* ${company}\n` +
                              `*Contact Person:* ${person}\n` +
                              `*Phone:* ${phone}\n` +
                              `*Corporate Email:* ${email}\n` +
                              `*Bandwidth:* ${bandwidth}\n` +
                              `*Location:* ${address}`;

            const btn = leasedLineForm.querySelector('button[type="submit"]');
            sendToTelegram(tgMessage, btn, "Thank you! Your Leased Line feasibility request has been submitted. Our technical team will deliver a proposal within 24 hours.");
        });
    }

    // 3. Corporate Broadband Form (corporate-broadband.html)
    const corpBroadbandForm = document.getElementById('corpBroadbandForm');
    if (corpBroadbandForm) {
        corpBroadbandForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const company = document.getElementById('corpCompany') ? document.getElementById('corpCompany').value.trim() : '';
            const person = document.getElementById('corpPerson') ? document.getElementById('corpPerson').value.trim() : '';
            const phone = document.getElementById('corpPhone') ? document.getElementById('corpPhone').value.trim() : '';
            const users = document.getElementById('corpUsers') ? document.getElementById('corpUsers').value : '';
            const address = document.getElementById('corpAddress') ? document.getElementById('corpAddress').value.trim() : '';

            const tgMessage = `*Corporate Broadband Request*\n\n` +
                              `*Business Name:* ${company}\n` +
                              `*Contact Person:* ${person}\n` +
                              `*Mobile Number:* ${phone}\n` +
                              `*Team Size:* ${users}\n` +
                              `*Office Address:* ${address}`;

            const btn = corpBroadbandForm.querySelector('button[type="submit"]');
            sendToTelegram(tgMessage, btn, "Thank you! Your Corporate Broadband feasibility request has been received. We will check route availability and send pricing shortly.");
        });
    }

    // 4. Modal Order Forms (.pricing-request-modal-form)
    const modalForms = document.querySelectorAll('.pricing-request-modal-form');
    modalForms.forEach(function(mForm) {
        mForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const pkgSelect = mForm.querySelector('.package-information select');
            const pkg = pkgSelect ? pkgSelect.value : 'Standard';
            const nameInput = mForm.querySelector('input[name="full-name"]');
            const name = nameInput ? nameInput.value.trim() : '';
            const phoneInput = mForm.querySelector('input[name="mobile-number"]');
            const phone = phoneInput ? phoneInput.value.trim() : '';
            const emailInput = mForm.querySelector('input[name="email"]');
            const email = emailInput ? (emailInput.value.trim() || 'Not provided') : 'Not provided';
            const addrInput = mForm.querySelector('input[name="home-address"]');
            const address = addrInput ? addrInput.value.trim() : '';
            const cableSelect = mForm.querySelector('select[name="line-cable-type"]') || mForm.querySelectorAll('.personal-information select')[0];
            const cable = cableSelect ? cableSelect.value : 'Optical fiber';

            const tgMessage = `*Broadband Plan Order*\n\n` +
                              `*Package:* ${pkg}\n` +
                              `*Name:* ${name}\n` +
                              `*Phone:* ${phone}\n` +
                              `*Email:* ${email}\n` +
                              `*Address:* ${address}\n` +
                              `*Cable Type:* ${cable}`;

            const btn = mForm.querySelector('button[type="submit"]');
            sendToTelegram(tgMessage, btn, "Thank you! Your order request has been received. Our team will verify installation feasibility.");
        });
    });

    // 5. Dynamic Footer Copyright Year (IST / Asia/Kolkata)
    function updateCopyrightYear() {
        try {
            var year = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Kolkata', year: 'numeric' }).format(new Date());
            var els = document.querySelectorAll('.current-year');
            for (var i = 0; i < els.length; i++) {
                els[i].textContent = year;
            }
        } catch (e) {
            var fallback = new Date().getFullYear();
            var els = document.querySelectorAll('.current-year');
            for (var i = 0; i < els.length; i++) {
                els[i].textContent = fallback;
            }
        }
    }
    updateCopyrightYear();
});
