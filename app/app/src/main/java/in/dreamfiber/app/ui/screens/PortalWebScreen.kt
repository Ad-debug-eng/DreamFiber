package `in`.dreamfiber.app.ui.screens

import android.annotation.SuppressLint
import android.content.Intent
import android.net.Uri
import android.view.ViewGroup
import android.webkit.CookieManager
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import `in`.dreamfiber.app.security.PinningClient
import `in`.dreamfiber.app.security.SecureStorage
import `in`.dreamfiber.app.ui.theme.DfBlue

/**
 * JS Bridge called automatically by pay.dreamfiber.in after login reaches dashboard.
 */
class PortalJsBridge(
    private val storage: SecureStorage,
    private val onAuthenticatedDashboard: (username: String) -> Unit,
    private val onLoggedOut: () -> Unit
) {
    @JavascriptInterface
    fun onPortalLoaded(username: String, customerName: String, planName: String, planExpiry: String) {
        if (username.isNotBlank()) storage.username = username
        if (customerName.isNotBlank()) storage.customerName = customerName
        if (planName.isNotBlank()) storage.planName = planName
        if (planExpiry.isNotBlank()) storage.planExpiry = planExpiry
        onAuthenticatedDashboard(username.ifBlank { storage.username })
    }

    @JavascriptInterface
    fun onPortalLoggedOut() {
        onLoggedOut()
    }
}

/**
 * Wraps https://pay.dreamfiber.in/ (keeping Turnstile, IP rate limiting, Omniware gateway & existing default/custom passwords intact)
 * and natively launches installed UPI apps (GPay, PhonePe, Paytm, BHIM) on upi:// or intent:// links.
 */
@SuppressLint("SetJavaScriptEnabled")
@Composable
fun PortalWebScreen(
    urlToLoad: String,
    storage: SecureStorage,
    onAuthenticatedDashboard: (username: String) -> Unit,
    onLoggedOut: () -> Unit,
    onWebViewReady: (WebView) -> Unit = {}
) {
    val context = LocalContext.current
    var progress by remember { mutableIntStateOf(0) }
    var webViewRef by remember { mutableStateOf<WebView?>(null) }

    BackHandler(enabled = webViewRef?.canGoBack() == true) {
        webViewRef?.goBack()
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                WebView(ctx).apply {
                    layoutParams = ViewGroup.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                    CookieManager.getInstance().setAcceptCookie(true)
                    CookieManager.getInstance().setAcceptThirdPartyCookies(this, true)

                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        databaseEnabled = true
                        loadWithOverviewMode = true
                        useWideViewPort = true
                        mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
                        userAgentString = "$userAgentString DreamFiberAndroidApp/1.0"
                    }

                    addJavascriptInterface(
                        PortalJsBridge(
                            storage = storage,
                            onAuthenticatedDashboard = onAuthenticatedDashboard,
                            onLoggedOut = onLoggedOut
                        ),
                        "DreamFiberBridge"
                    )

                    webChromeClient = object : WebChromeClient() {
                        override fun onProgressChanged(view: WebView?, newProgress: Int) {
                            progress = newProgress
                        }
                    }

                    webViewClient = object : WebViewClient() {
                        override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                            val u = request?.url ?: return false
                            val str = u.toString()
                            val scheme = (u.scheme ?: "").lowercase()

                            // Launch UPI apps (GPay, PhonePe, Paytm, BHIM), phone dialer, email, or WhatsApp natively
                            if (scheme in listOf("upi", "tez", "phonepe", "paytmmp", "bhim", "tel", "mailto", "whatsapp") ||
                                str.startsWith("https://wa.me/") ||
                                str.startsWith("https://api.whatsapp.com/")
                            ) {
                                return launchExternalSafe(ctx, str)
                            }

                            if (scheme == "intent") {
                                return launchIntentUri(ctx, str)
                            }

                            // Keep pay.dreamfiber.in, dreamfiber.in & Omniware 3DS bank flows smoothly inside WebView
                            return false
                        }

                        override fun onPageFinished(view: WebView?, url: String?) {
                            super.onPageFinished(view, url)
                            CookieManager.getInstance().flush()
                            val u = url ?: return
                            val trimmed = u.trimEnd('/')
                            if (trimmed == PinningClient.PORTAL_BASE || u.contains("page=login") || u.contains("page=logout")) {
                                onLoggedOut()
                                return
                            }
                            if (u.startsWith("${PinningClient.PORTAL_BASE}/index.php")) {
                                // Check cookie & DOM fallback in case portal page loaded synchronously
                                val cookies = CookieManager.getInstance().getCookie(PinningClient.PORTAL_BASE) ?: ""
                                val match = Regex("(?:^|;\\s*)df_user=([^;]+)").find(cookies)
                                val cookieUser = match?.groupValues?.getOrNull(1)?.let {
                                    try { java.net.URLDecoder.decode(it, "UTF-8") } catch (_: Exception) { it }
                                } ?: ""
                                if (cookieUser.isNotBlank()) {
                                    storage.username = cookieUser
                                }
                                onAuthenticatedDashboard(storage.username)
                            }
                        }
                    }

                    loadUrl(urlToLoad)
                    webViewRef = this
                    onWebViewReady(this)
                }
            }
        )

        if (progress in 1..99) {
            LinearProgressIndicator(
                progress = { progress / 100f },
                color = DfBlue,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

private fun launchExternalSafe(context: android.content.Context, url: String): Boolean {
    return try {
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url)).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
        true
    } catch (_: Exception) {
        true
    }
}

private fun launchIntentUri(context: android.content.Context, intentUri: String): Boolean {
    return try {
        val intent = Intent.parseUri(intentUri, Intent.URI_INTENT_SCHEME).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        if (intent.resolveActivity(context.packageManager) != null) {
            context.startActivity(intent)
            true
        } else {
            val fallback = intent.getStringExtra("browser_fallback_url")
            if (!fallback.isNullOrBlank()) {
                launchExternalSafe(context, fallback)
            }
            true
        }
    } catch (_: Exception) {
        true
    }
}
