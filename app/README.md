# DreamFiber Mobile App (`app/`)

This directory contains the native **Android (Kotlin + Jetpack Compose)** DreamFiber Customer Self-Care Application (`in.dreamfiber.app`), built against Android SDK 34 with ProGuard/R8 hardening, TLS Certificate Pinning, Android Keystore `EncryptedSharedPreferences`, Firebase Cloud Messaging (`BigPictureStyle` rich image support), Biometric Unlock, UPI Intent (`GPay`/`PhonePe`/`Paytm`/`BHIM`), and foreground Location/ISP/Device telemetry.

## Quick Setup for Push Notifications & Play Store Release
1. **Lock-Screen Rich Image Push (Firebase Cloud Messaging):**
   - Create a free project in Firebase Console and register Android package `in.dreamfiber.app`.
   - Download `google-services.json` and place it at [`app/google-services.json`](./app/google-services.json) (automatically ignored by `.gitignore`; Gradle applies the Google Services plugin automatically when present).
   - Generate a Firebase Service Account JSON key (`Project Settings → Service accounts → Generate new private key`) and upload it securely to the Cloudflare Worker (never inside the APK):
     ```powershell
     cd ../website/portal-worker
     Get-Content path\to\firebase-service-account.json -Raw | npx wrangler secret put FCM_SERVICE_ACCOUNT_JSON
     ```
2. **Admin Telemetry & Notification Center:**
   - Access live customer locations (with Google Maps links), ISP checks, CSV/Excel exports, Festival/Offer image push broadcasts, and configurable Pre/Post-Expiry schedules at **`https://pay.dreamfiber.in/admin`**.
   - Change your admin password anytime via `npx wrangler secret put ADMIN_PASSWORD`.
3. **Play Store Release Signing:**
   - Generate a private upload keystore (kept outside Git) and sign the release bundle with `./gradlew.bat bundleRelease`.

> **Project Structure**
> - [`../website/`](../website/): DreamFiber main static website (`dreamfiber.in`), Account Deletion page (`delete-account.html`), & Cloudflare Worker (`pay.dreamfiber.in`, `/admin`, D1 telemetry DB, daily Cron).
> - [`./`](./): Native Android Kotlin/Compose project (`app/`).

---

## Pre-Development Checklist: Building a Great & Secure App

### 1. Push Notifications (Festivals, Offers & Automated Expiry Alerts)
- **Rich Image Notifications (Yes! Supported):**
  - Powered by **Firebase Cloud Messaging (FCM)** using Android `BigPictureStyle` & iOS `UNNotificationAttachment`.
  - Supports **Title + Body + High-Res Banner Image** (recommended `1024x512` JPG/PNG < 300 KB over HTTPS) + **Deep Link** (tapping opens directly to Offer / Plan Upgrade / Pay Now).
- **Festival & Offer Broadcasts:**
  - Admin web dashboard to upload an offer/festival poster, target **All Subscribers**, **Active Only**, or **Expired Only**, and send immediately or schedule.
- **Configurable Recharge Expiry Reminders (Pre- & Post-Expiry):**
  - Admin configures offsets dynamically without updating the app (example for a plan ending **Jan 1**):
    - **Before Expiry ("About to end"):** e.g. `-5 days`, `-2 days`, `-1 day`, `On expiry day (9:00 AM)`.
    - **After Expiry ("Recharge has ended"):** e.g. `+1 day`, `+3 days`, `+7 days`.
  - **Auto-Cancel Logic:** Daily scheduler checks live expiry date before sending—if the customer already renewed, pending expiry reminders are skipped automatically.
  - **Quiet Hours:** Automated reminders run during polite daytime hours (e.g. `10:00 AM` or `6:00 PM IST`), never overnight.
  - **In-App Notification Inbox:** Bell icon inside the app preserves offers & expiry alerts even if cleared from the phone's notification tray.

### 2. Application Security & Authentication
- **Replace Weak Default Passwords (`123456`):**
  - Implement **Mobile OTP Login** (SMS / WhatsApp OTP to registered mobile) OR require password change on first login so knowledge of `username` alone never grants access.
- **Encrypted Credential Storage:**
  - Use **Android Keystore / EncryptedSharedPreferences** (`flutter_secure_storage`), never plain `SharedPreferences` or unencrypted local storage.
- **Transport & Proxy Protection:**
  - Enforce HTTPS-only (`usesCleartextTraffic="false"`).
  - Add **SSL Certificate Pinning** on API endpoints to block MITM traffic interception.
- **APK Hardening:**
  - Enable **R8 / ProGuard** code obfuscation & shrinking.
  - Enable **Google Play Integrity API** & root/tamper detection.
  - Zero hardcoded secrets (no Cloudflare keys, gateway secret keys, or Firebase server keys inside APK).

### 3. Payments & Payment Gateway Security
- **Direct UPI Intent Support:** Launch GPay, PhonePe, Paytm, or BHIM directly via `upi://pay` and return seamlessly to the app.
- **Server-Side Payment Verification:** Always verify payment status via **Payment Gateway Webhooks + Server Signature Check** before marking an invoice paid or triggering renewal.
- **Google Play Billing Exemption:** ISP / Broadband utility bill payments are exempt from Google Play's 15–30% digital goods fee (declare as Physical/Utility Services; do not sell standalone non-ISP digital content via external gateway).

### 4. Google Play Store Compliance (Avoid Rejections)
- **Organization Play Console Account:** Register under **Dream Cable and Internet Services Private Limited** (with D-U-N-S number) to bypass personal-account 12-tester closed testing rules.
- **Location Policy:** Request **Foreground-Only** location (`ACCESS_FINE_LOCATION` *"While using the app"*), NEVER `ACCESS_BACKGROUND_LOCATION` (*"Allow all the time"*), and pair with Wi-Fi + IP verification so outdoor recharges don't corrupt ONU coordinates.
- **Account & Data Deletion URL:** Mandatory both inside app settings and on a public `dreamfiber.in` webpage.
- **Android 13+ Notification Prompt:** Show a friendly pre-permission explanation before triggering the system `POST_NOTIFICATIONS` popup.
- **Compliance Links:** Link directly to `dreamfiber.in` **Terms**, **Refunds (5–7 business days)**, **Privacy Policy**, **Plans (INR)**, and **Contact Us**.

### 5. Backend Database & Scheduler Requirements
- **Subscriber Sync & Telemetry DB** (e.g., Cloudflare D1 / Supabase / PostgreSQL):
  - `username`, `fcm_device_tokens[]`, `plan_expiry_date`, `last_known_ip`, `notification_opt_ins`.
- **Daily Cron Trigger** (e.g., Cloudflare Worker Cron at 10:00 AM IST): Computes expiry offsets and triggers FCM v1 API.
- **Monitoring & Crash Analytics:** Firebase Crashlytics + structured API error logging.
