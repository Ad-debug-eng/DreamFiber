package `in`.dreamfiber.app.telemetry

import android.annotation.SuppressLint
import android.app.ActivityManager
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.location.Location
import android.net.ConnectivityManager
import android.net.LinkProperties
import android.net.NetworkCapabilities
import android.net.wifi.WifiManager
import android.os.BatteryManager
import android.os.Build
import android.os.Environment
import android.os.StatFs
import android.provider.Settings
import android.text.format.Formatter
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import `in`.dreamfiber.app.BuildConfig
import `in`.dreamfiber.app.security.PinningClient
import `in`.dreamfiber.app.security.SecureStorage
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import org.json.JSONObject
import java.io.File
import java.net.Inet4Address
import java.security.MessageDigest
import java.util.Locale
import kotlin.coroutines.resume

/**
 * Collects Google-Play-compliant foreground Location, Wi-Fi, ISP, Device Hardware,
 * and App Integrity telemetry, and delivers it over TLS-pinned HTTPS.
 */
object TelemetryCollector {

    @SuppressLint("MissingPermission")
    suspend fun getFreshLocation(context: Context): Location? {
        val fine = ContextCompat.checkSelfPermission(
            context, android.Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
        val coarse = ContextCompat.checkSelfPermission(
            context, android.Manifest.permission.ACCESS_COARSE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
        if (!fine && !coarse) return null

        val client = LocationServices.getFusedLocationProviderClient(context)

        val current = withTimeoutOrNull(9000L) {
            suspendCancellableCoroutine<Location?> { cont ->
                val cts = CancellationTokenSource()
                cont.invokeOnCancellation { cts.cancel() }
                client.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, cts.token)
                    .addOnSuccessListener { loc -> if (cont.isActive) cont.resume(loc) }
                    .addOnFailureListener { if (cont.isActive) cont.resume(null) }
            }
        }
        if (current != null) return current

        return withTimeoutOrNull(3000L) {
            suspendCancellableCoroutine<Location?> { cont ->
                client.lastLocation
                    .addOnSuccessListener { loc -> if (cont.isActive) cont.resume(loc) }
                    .addOnFailureListener { if (cont.isActive) cont.resume(null) }
            }
        }
    }

    suspend fun collectAndSend(
        context: Context,
        storage: SecureStorage,
        eventType: String,
        location: Location? = null
    ): JSONObject? = withContext(Dispatchers.IO) {
        val payload = JSONObject()
        payload.put("source", "app")
        payload.put("event_type", eventType)
        payload.put("username", storage.username)
        payload.put("customer_name", storage.customerName)
        payload.put("plan_name", storage.planName)
        payload.put("plan_expiry", storage.planExpiry)
        payload.put("fcm_token", storage.fcmToken)
        payload.put("notifications_enabled", NotificationManagerCompat.from(context).areNotificationsEnabled())

        if (location != null) {
            payload.put("lat", location.latitude)
            payload.put("lng", location.longitude)
            payload.put("accuracy_m", location.accuracy.toDouble())
            if (location.hasAltitude()) payload.put("altitude", location.altitude)
            val isMock = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                location.isMock
            } else {
                @Suppress("DEPRECATION")
                location.isFromMockProvider
            }
            payload.put("is_mock_location", isMock)
        }

        fillNetworkFields(context, payload)
        fillDeviceFields(context, payload)

        val response = PinningClient.postTelemetry(payload)
        if (response != null && response.optBoolean("success", false)) {
            storage.lastIp = response.optString("ip_address", storage.lastIp)
            storage.lastIsp = response.optString("isp_name", storage.lastIsp)
            storage.isOnDreamFiberNet = response.optBoolean("is_dreamfiber_net", storage.isOnDreamFiberNet)
            if (location != null) {
                storage.lastCoords = "${String.format(Locale.US, "%.5f", location.latitude)}, ${String.format(Locale.US, "%.5f", location.longitude)}"
            }
        }
        response
    }

    @Suppress("DEPRECATION")
    private fun fillNetworkFields(context: Context, payload: JSONObject) {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager
        val activeNet = cm?.activeNetwork
        val caps = cm?.getNetworkCapabilities(activeNet)

        val transport = when {
            caps == null -> "Offline"
            caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> "WiFi"
            caps.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> "Cellular"
            caps.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> "Ethernet"
            else -> "Other"
        }
        val vpnActive = caps?.hasTransport(NetworkCapabilities.TRANSPORT_VPN) == true
        payload.put("network_type", transport)
        payload.put("vpn_active", vpnActive)

        if (caps != null) {
            val downMbps = caps.linkDownstreamBandwidthKbps / 1000.0
            if (downMbps > 0) payload.put("downlink_mbps", downMbps)
        }

        // Local IP from active LinkProperties
        try {
            val lp: LinkProperties? = cm?.getLinkProperties(activeNet)
            val localAddr = lp?.linkAddresses?.firstOrNull { it.address is Inet4Address }?.address?.hostAddress
            if (!localAddr.isNullOrBlank()) payload.put("local_ip", localAddr)
            val gw = lp?.routes?.firstOrNull { it.isDefaultRoute && it.gateway is Inet4Address }?.gateway?.hostAddress
            if (!gw.isNullOrBlank()) payload.put("gateway_ip", gw)
        } catch (_: Exception) {}

        // Wi-Fi SSID / BSSID (available when Wi-Fi connected & location granted)
        try {
            val wm = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as? WifiManager
            val info = wm?.connectionInfo
            if (info != null) {
                val rawSsid = info.ssid?.trim('"') ?: ""
                if (rawSsid.isNotBlank() && rawSsid != "<unknown ssid>") {
                    payload.put("wifi_ssid", rawSsid)
                }
                val bssid = info.bssid ?: ""
                if (bssid.isNotBlank() && bssid != "02:00:00:00:00:00") {
                    payload.put("wifi_bssid", bssid)
                }
                if (!payload.has("gateway_ip")) {
                    val dhcpGw = wm.dhcpInfo?.gateway ?: 0
                    if (dhcpGw != 0) payload.put("gateway_ip", Formatter.formatIpAddress(dhcpGw))
                }
            }
        } catch (_: Exception) {}
    }

    private fun fillDeviceFields(context: Context, payload: JSONObject) {
        payload.put("device_brand", Build.MANUFACTURER)
        payload.put("device_model", Build.MODEL)
        payload.put("os_name", "Android")
        payload.put("os_version", "Android ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})")
        payload.put("app_version", "${BuildConfig.VERSION_NAME} (${BuildConfig.VERSION_CODE})")
        payload.put("install_source", getInstallSource(context))
        payload.put("device_id", getHashedAndroidId(context))

        val dm = context.resources.displayMetrics
        payload.put("screen_res", "${dm.widthPixels}x${dm.heightPixels}@${dm.densityDpi}dpi")

        try {
            val am = context.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
            val memInfo = ActivityManager.MemoryInfo()
            am?.getMemoryInfo(memInfo)
            payload.put("ram_mb", (memInfo.totalMem / (1024L * 1024L)).toInt())
        } catch (_: Exception) {}

        try {
            val stat = StatFs(Environment.getDataDirectory().path)
            payload.put("storage_free_mb", (stat.availableBytes / (1024L * 1024L)).toInt())
        } catch (_: Exception) {}

        payload.put("cpu_cores", Runtime.getRuntime().availableProcessors())

        try {
            val batIntent = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
            val level = batIntent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            val scale = batIntent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
            if (level >= 0 && scale > 0) {
                payload.put("battery_pct", ((level * 100f) / scale).toInt())
            }
            val status = batIntent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
            val charging = status == BatteryManager.BATTERY_STATUS_CHARGING || status == BatteryManager.BATTERY_STATUS_FULL
            payload.put("is_charging", charging)
        } catch (_: Exception) {}

        payload.put("is_rooted", isDeviceRooted())
        payload.put("language", Locale.getDefault().toLanguageTag())
    }

    private fun getInstallSource(context: Context): String {
        return try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                context.packageManager.getInstallSourceInfo(context.packageName).installingPackageName ?: "sideload"
            } else {
                @Suppress("DEPRECATION")
                context.packageManager.getInstallerPackageName(context.packageName) ?: "sideload"
            }
        } catch (_: Exception) {
            "unknown"
        }
    }

    @SuppressLint("HardwareIds")
    private fun getHashedAndroidId(context: Context): String {
        return try {
            val raw = Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID) ?: "unknown"
            val digest = MessageDigest.getInstance("SHA-256").digest(raw.toByteArray())
            digest.joinToString("") { "%02x".format(it) }.take(32)
        } catch (_: Exception) {
            ""
        }
    }

    private fun isDeviceRooted(): Boolean {
        val tags = Build.TAGS
        if (tags != null && tags.contains("test-keys")) return true
        val paths = arrayOf(
            "/system/app/Superuser.apk",
            "/sbin/su",
            "/system/bin/su",
            "/system/xbin/su",
            "/data/local/xbin/su",
            "/data/local/bin/su",
            "/su/bin/su"
        )
        return paths.any { File(it).exists() }
    }
}
