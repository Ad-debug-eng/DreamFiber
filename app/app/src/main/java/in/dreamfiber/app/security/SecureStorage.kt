package `in`.dreamfiber.app.security

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

/**
 * Hardware-backed Encrypted SharedPreferences (Android Keystore AES256-GCM).
 * Replaces plain SharedPreferences so local subscriber metadata is unreadable if extracted.
 */
class SecureStorage(context: Context) {

    private val prefs: SharedPreferences

    init {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()

        prefs = EncryptedSharedPreferences.create(
            context,
            "dreamfiber_secure_vault",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    var username: String
        get() = prefs.getString(KEY_USERNAME, "") ?: ""
        set(value) = prefs.edit().putString(KEY_USERNAME, value).apply()

    var customerName: String
        get() = prefs.getString(KEY_CUSTOMER_NAME, "") ?: ""
        set(value) = prefs.edit().putString(KEY_CUSTOMER_NAME, value).apply()

    var planName: String
        get() = prefs.getString(KEY_PLAN_NAME, "") ?: ""
        set(value) = prefs.edit().putString(KEY_PLAN_NAME, value).apply()

    var planExpiry: String
        get() = prefs.getString(KEY_PLAN_EXPIRY, "") ?: ""
        set(value) = prefs.edit().putString(KEY_PLAN_EXPIRY, value).apply()

    var fcmToken: String
        get() = prefs.getString(KEY_FCM_TOKEN, "") ?: ""
        set(value) = prefs.edit().putString(KEY_FCM_TOKEN, value).apply()

    var biometricLockEnabled: Boolean
        get() = prefs.getBoolean(KEY_BIOMETRIC, false)
        set(value) = prefs.edit().putBoolean(KEY_BIOMETRIC, value).apply()

    var notifPrePromptShown: Boolean
        get() = prefs.getBoolean(KEY_NOTIF_PROMPTED, false)
        set(value) = prefs.edit().putBoolean(KEY_NOTIF_PROMPTED, value).apply()

    var lastIp: String
        get() = prefs.getString(KEY_LAST_IP, "") ?: ""
        set(value) = prefs.edit().putString(KEY_LAST_IP, value).apply()

    var lastIsp: String
        get() = prefs.getString(KEY_LAST_ISP, "") ?: ""
        set(value) = prefs.edit().putString(KEY_LAST_ISP, value).apply()

    var isOnDreamFiberNet: Boolean
        get() = prefs.getBoolean(KEY_IS_DF_NET, false)
        set(value) = prefs.edit().putBoolean(KEY_IS_DF_NET, value).apply()

    var lastCoords: String
        get() = prefs.getString(KEY_LAST_COORDS, "") ?: ""
        set(value) = prefs.edit().putString(KEY_LAST_COORDS, value).apply()

    fun clearSession() {
        prefs.edit()
            .remove(KEY_USERNAME)
            .remove(KEY_CUSTOMER_NAME)
            .remove(KEY_PLAN_NAME)
            .remove(KEY_PLAN_EXPIRY)
            .apply()
    }

    fun wipeAllAppVault() {
        prefs.edit().clear().apply()
    }

    companion object {
        private const val KEY_USERNAME = "username"
        private const val KEY_CUSTOMER_NAME = "customer_name"
        private const val KEY_PLAN_NAME = "plan_name"
        private const val KEY_PLAN_EXPIRY = "plan_expiry"
        private const val KEY_FCM_TOKEN = "fcm_token"
        private const val KEY_BIOMETRIC = "biometric_enabled"
        private const val KEY_NOTIF_PROMPTED = "notif_pre_prompt_shown"
        private const val KEY_LAST_IP = "last_ip"
        private const val KEY_LAST_ISP = "last_isp"
        private const val KEY_IS_DF_NET = "is_df_net"
        private const val KEY_LAST_COORDS = "last_coords"
    }
}
