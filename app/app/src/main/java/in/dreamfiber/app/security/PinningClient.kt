package `in`.dreamfiber.app.security

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.CertificatePinner
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

data class AppRemoteConfig(
    val requireLocationGate: Boolean = true,
    val ip: String = "",
    val isp: String = "",
    val asn: Int = 0,
    val isDreamFiberNet: Boolean = false,
    val city: String = ""
)

data class InboxNotification(
    val id: Long,
    val createdAt: String,
    val campaignType: String,
    val title: String,
    val body: String,
    val imageUrl: String,
    val deepLink: String
)

/**
 * TLS-Pinned HTTPS Client for DreamFiber API endpoints.
 * Pins active Cloudflare leaf + Let's Encrypt / GTS Root CAs to block MITM proxy inspection.
 * Zero secrets are embedded in the APK.
 */
object PinningClient {

    const val PORTAL_BASE = "https://pay.dreamfiber.in"
    const val WEBSITE_BASE = "https://dreamfiber.in"

    private val pinner = CertificatePinner.Builder()
        .add("pay.dreamfiber.in", "sha256/DPHIXxcFJ9uNWbeYX9F5Rx14ycF2ivZeQRmrIxENiNw=")
        .add("pay.dreamfiber.in", "sha256/diGVwiVYbubAI3RW4hB9xU8e/CH2GnkuvVFZE8zmgzI=") // ISRG Root X2
        .add("pay.dreamfiber.in", "sha256/C5+lpZ7tcVwmwQIMcRtPbsQtWLABXhQzejna0wHFr8M=") // ISRG Root X1
        .add("pay.dreamfiber.in", "sha256/hxqRlPTu1bMS/0DITB1SSu0vd4u/8l8TjPgfaAp63Gc=") // GTS Root R1
        .add("pay.dreamfiber.in", "sha256/mEflZT5enoR1FuXLgYYGqnVEoZvmf9c2bVBpiOjYQ0c=") // GTS Root R4
        .add("dreamfiber.in", "sha256/diGVwiVYbubAI3RW4hB9xU8e/CH2GnkuvVFZE8zmgzI=")
        .add("dreamfiber.in", "sha256/C5+lpZ7tcVwmwQIMcRtPbsQtWLABXhQzejna0wHFr8M=")
        .add("dreamfiber.in", "sha256/hxqRlPTu1bMS/0DITB1SSu0vd4u/8l8TjPgfaAp63Gc=")
        .add("dreamfiber.in", "sha256/mEflZT5enoR1FuXLgYYGqnVEoZvmf9c2bVBpiOjYQ0c=")
        .build()

    val client: OkHttpClient = OkHttpClient.Builder()
        .certificatePinner(pinner)
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .writeTimeout(15, TimeUnit.SECONDS)
        .build()

    private val JSON_MEDIA = "application/json; charset=utf-8".toMediaType()

    suspend fun fetchAppConfig(): AppRemoteConfig = withContext(Dispatchers.IO) {
        try {
            val req = Request.Builder().url("$PORTAL_BASE/api/app-config").get().build()
            client.newCall(req).execute().use { resp ->
                if (!resp.isSuccessful) return@withContext AppRemoteConfig()
                val raw = resp.body?.string() ?: return@withContext AppRemoteConfig()
                val js = JSONObject(raw)
                val net = js.optJSONObject("network_probe")
                AppRemoteConfig(
                    requireLocationGate = js.optBoolean("require_location_gate", true),
                    ip = net?.optString("ip", "") ?: "",
                    isp = net?.optString("isp", "") ?: "",
                    asn = net?.optInt("asn", 0) ?: 0,
                    isDreamFiberNet = net?.optBoolean("is_dreamfiber_net", false) ?: false,
                    city = net?.optString("city", "") ?: ""
                )
            }
        } catch (_: Exception) {
            AppRemoteConfig()
        }
    }

    suspend fun postTelemetry(payload: JSONObject): JSONObject? = withContext(Dispatchers.IO) {
        try {
            val req = Request.Builder()
                .url("$PORTAL_BASE/api/telemetry")
                .post(payload.toString().toRequestBody(JSON_MEDIA))
                .build()
            client.newCall(req).execute().use { resp ->
                val raw = resp.body?.string() ?: return@withContext null
                JSONObject(raw)
            }
        } catch (_: Exception) {
            null
        }
    }

    suspend fun fetchInbox(username: String): List<InboxNotification> = withContext(Dispatchers.IO) {
        try {
            val encodedUser = java.net.URLEncoder.encode(username, "UTF-8")
            val req = Request.Builder()
                .url("$PORTAL_BASE/api/notifications/inbox?username=$encodedUser")
                .get()
                .build()
            client.newCall(req).execute().use { resp ->
                if (!resp.isSuccessful) return@withContext emptyList()
                val raw = resp.body?.string() ?: return@withContext emptyList()
                val js = JSONObject(raw)
                val arr: JSONArray = js.optJSONArray("notifications") ?: return@withContext emptyList()
                val out = mutableListOf<InboxNotification>()
                for (i in 0 until arr.length()) {
                    val o = arr.getJSONObject(i)
                    out.add(
                        InboxNotification(
                            id = o.optLong("id", i.toLong()),
                            createdAt = o.optString("created_at", ""),
                            campaignType = o.optString("campaign_type", "offer"),
                            title = o.optString("title", ""),
                            body = o.optString("body", ""),
                            imageUrl = o.optString("image_url", ""),
                            deepLink = o.optString("deep_link", "home")
                        )
                    )
                }
                out
            }
        } catch (_: Exception) {
            emptyList()
        }
    }

    suspend fun submitDeletionRequest(
        username: String,
        mobile: String,
        reason: String
    ): Pair<Boolean, String> = withContext(Dispatchers.IO) {
        try {
            val body = JSONObject().apply {
                put("username", username)
                put("mobile", mobile)
                put("reason", reason)
                put("source", "app")
            }
            val req = Request.Builder()
                .url("$PORTAL_BASE/api/account-deletion")
                .post(body.toString().toRequestBody(JSON_MEDIA))
                .build()
            client.newCall(req).execute().use { resp ->
                val raw = resp.body?.string() ?: "{}"
                val js = JSONObject(raw)
                val ok = resp.isSuccessful && js.optBoolean("success", false)
                val msg = if (ok) {
                    "Ticket ${js.optString("ticket_id")}: ${js.optString("message")}"
                } else {
                    js.optString("error", "Unable to submit request.")
                }
                ok to msg
            }
        } catch (e: Exception) {
            false to "Network error: ${e.localizedMessage ?: "Try again"}"
        }
    }
}
