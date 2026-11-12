package `in`.dreamfiber.app.notifications

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import `in`.dreamfiber.app.MainActivity
import `in`.dreamfiber.app.R
import `in`.dreamfiber.app.security.PinningClient
import `in`.dreamfiber.app.security.SecureStorage
import `in`.dreamfiber.app.telemetry.TelemetryCollector
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.Request

object NotificationChannels {
    const val CHANNEL_OFFERS = "offers_festivals"
    const val CHANNEL_EXPIRY = "expiry_reminders"
    const val CHANNEL_ALERTS = "service_alerts"

    fun ensureCreated(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager ?: return
        val channels = listOf(
            NotificationChannel(CHANNEL_OFFERS, "Offers & Festival Greetings", NotificationManager.IMPORTANCE_HIGH).apply {
                description = "Seasonal broadband offers, festival wishes & OTT bundles with banners."
            },
            NotificationChannel(CHANNEL_EXPIRY, "Recharge Expiry Reminders", NotificationManager.IMPORTANCE_HIGH).apply {
                description = "Alerts before and after your broadband plan expires."
            },
            NotificationChannel(CHANNEL_ALERTS, "Network & Service Alerts", NotificationManager.IMPORTANCE_DEFAULT).apply {
                description = "Important maintenance notices and outage restoration updates."
            }
        )
        nm.createNotificationChannels(channels)
    }
}

/**
 * Handles Firebase Cloud Messaging push payloads with optional Rich Banner Images (BigPictureStyle)
 * and deep-link routing into Pay Bill, Plans, or Alerts Inbox.
 */
class DreamFiberMessagingService : FirebaseMessagingService() {

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        val storage = SecureStorage(applicationContext)
        storage.fcmToken = token
        if (storage.username.isNotBlank()) {
            CoroutineScope(Dispatchers.IO).launch {
                TelemetryCollector.collectAndSend(applicationContext, storage, "fcm_token_refresh", null)
            }
        }
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        NotificationChannels.ensureCreated(applicationContext)

        val data = remoteMessage.data
        val notif = remoteMessage.notification
        val title = data["title"] ?: notif?.title ?: "DreamFiber"
        val body = data["body"] ?: notif?.body ?: ""
        val imageUrl = data["image_url"]?.takeIf { it.isNotBlank() } ?: notif?.imageUrl?.toString() ?: ""
        val deepLink = data["deep_link"] ?: "home"
        val campaignType = data["campaign_type"] ?: "offer"

        val channelId = when (campaignType) {
            "expiry_auto" -> NotificationChannels.CHANNEL_EXPIRY
            "outage" -> NotificationChannels.CHANNEL_ALERTS
            else -> NotificationChannels.CHANNEL_OFFERS
        }

        val tapIntent = Intent(applicationContext, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
            putExtra("deep_link", deepLink)
        }
        val pi = PendingIntent.getActivity(
            applicationContext,
            System.currentTimeMillis().toInt(),
            tapIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(applicationContext, channelId)
            .setSmallIcon(R.drawable.df_logo)
            .setContentTitle(title)
            .setContentText(body)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pi)

        val bitmap = if (imageUrl.startsWith("https://")) downloadBannerBitmap(imageUrl) else null
        if (bitmap != null) {
            builder.setLargeIcon(bitmap)
            builder.setStyle(
                NotificationCompat.BigPictureStyle()
                    .bigPicture(bitmap)
                    .bigLargeIcon(null as Bitmap?)
                    .setSummaryText(body)
            )
        } else {
            builder.setStyle(NotificationCompat.BigTextStyle().bigText(body))
        }

        val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        nm.notify((System.currentTimeMillis() % Int.MAX_VALUE).toInt(), builder.build())
    }

    private fun downloadBannerBitmap(url: String): Bitmap? {
        return try {
            val req = Request.Builder().url(url).get().build()
            PinningClient.client.newCall(req).execute().use { resp ->
                if (!resp.isSuccessful) return null
                resp.body?.byteStream()?.use { BitmapFactory.decodeStream(it) }
            }
        } catch (_: Exception) {
            null
        }
    }
}
