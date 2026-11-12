package `in`.dreamfiber.app

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.webkit.CookieManager
import androidx.activity.compose.setContent
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import androidx.lifecycle.lifecycleScope
import com.google.firebase.FirebaseApp
import com.google.firebase.messaging.FirebaseMessaging
import `in`.dreamfiber.app.notifications.NotificationChannels
import `in`.dreamfiber.app.security.PinningClient
import `in`.dreamfiber.app.security.SecureStorage
import `in`.dreamfiber.app.telemetry.TelemetryCollector
import `in`.dreamfiber.app.ui.screens.AlertsInboxScreen
import `in`.dreamfiber.app.ui.screens.LocationGateScreen
import `in`.dreamfiber.app.ui.screens.NotificationPrePromptScreen
import `in`.dreamfiber.app.ui.screens.PortalWebScreen
import `in`.dreamfiber.app.ui.screens.SupportSettingsScreen
import `in`.dreamfiber.app.ui.theme.DreamFiberTheme
import `in`.dreamfiber.app.ui.theme.DfBlue
import `in`.dreamfiber.app.ui.theme.DfNavy
import kotlinx.coroutines.launch

class MainActivity : FragmentActivity() {

    private lateinit var storage: SecureStorage
    private var deepLinkTab by mutableIntStateOf(0)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        storage = SecureStorage(applicationContext)
        NotificationChannels.ensureCreated(applicationContext)
        fetchFcmTokenIfInitialized()
        handleIntentDeepLink(intent)

        setContent {
            DreamFiberTheme {
                DreamFiberRootApp()
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handleIntentDeepLink(intent)
    }

    private fun handleIntentDeepLink(intent: Intent?) {
        val link = intent?.getStringExtra("deep_link") ?: return
        deepLinkTab = when (link) {
            "plans" -> 1
            "inbox" -> 2
            "pay", "home" -> 0
            else -> 0
        }
    }

    private fun fetchFcmTokenIfInitialized() {
        try {
            if (FirebaseApp.getApps(applicationContext).isNotEmpty()) {
                FirebaseMessaging.getInstance().token.addOnSuccessListener { token ->
                    if (!token.isNullOrBlank()) {
                        storage.fcmToken = token
                    }
                }
            }
        } catch (_: Exception) {
            // Firebase google-services.json not added yet; app runs cleanly via In-App Inbox until configured
        }
    }

    @Composable
    private fun DreamFiberRootApp() {
        var biometricPassed by remember { mutableStateOf(!storage.biometricLockEnabled || storage.username.isBlank()) }
        var isAuthenticated by remember { mutableStateOf(false) }
        var requireLocationGate by remember { mutableStateOf(true) }
        var locationVerifiedInSession by remember { mutableStateOf(false) }
        var notifPromptDone by remember { mutableStateOf(storage.notifPrePromptShown || hasNotifPermission()) }
        var portalSessionNonce by remember { mutableIntStateOf(0) }

        LaunchedEffect(Unit) {
            val cfg = PinningClient.fetchAppConfig()
            requireLocationGate = cfg.requireLocationGate
            if (cfg.ip.isNotBlank()) storage.lastIp = cfg.ip
            if (cfg.isp.isNotBlank()) storage.lastIsp = cfg.isp
            storage.isOnDreamFiberNet = cfg.isDreamFiberNet
        }

        // 1. Optional Biometric Lock Gate
        if (!biometricPassed) {
            BiometricLockOverlay(
                onUnlockSuccess = { biometricPassed = true },
                onTriggerPrompt = { showBiometricPrompt(onSuccess = { biometricPassed = true }) }
            )
            return
        }

        // 2. Mandatory Post-Login "Verify your Dream Fiber connection" Location Gate
        if (isAuthenticated && requireLocationGate && !locationVerifiedInSession) {
            LocationGateScreen(
                storage = storage,
                onVerified = { locationVerifiedInSession = true }
            )
            return
        }

        // 3. Friendly Android 13+ Pre-Permission Explanation before system POST_NOTIFICATIONS popup
        if (isAuthenticated && (!requireLocationGate || locationVerifiedInSession) && !notifPromptDone) {
            NotificationPrePromptScreen(
                storage = storage,
                onDone = { notifPromptDone = true }
            )
            return
        }

        // 4. Main App Shell (Login screen -> Authenticated 4-Tab Dashboard)
        val hasSavedCookie = CookieManager.getInstance()
            .getCookie(PinningClient.PORTAL_BASE)
            ?.contains("PHPSESSID=") == true
        val portalEntryUrl = if (hasSavedCookie && storage.username.isNotBlank()) {
            "${PinningClient.PORTAL_BASE}/index.php"
        } else {
            "${PinningClient.PORTAL_BASE}/"
        }

        if (!isAuthenticated) {
            key(portalSessionNonce) {
                PortalWebScreen(
                    urlToLoad = portalEntryUrl,
                    storage = storage,
                    onAuthenticatedDashboard = {
                        isAuthenticated = true
                        if (!requireLocationGate) {
                            lifecycleScope.launch {
                                TelemetryCollector.collectAndSend(applicationContext, storage, "dashboard_sync", null)
                            }
                        }
                    },
                    onLoggedOut = {
                        isAuthenticated = false
                        locationVerifiedInSession = false
                    }
                )
            }
            return
        }

        Scaffold(
            bottomBar = {
                NavigationBar {
                    NavigationBarItem(
                        selected = deepLinkTab == 0,
                        onClick = { deepLinkTab = 0 },
                        icon = { Icon(Icons.Rounded.Home, contentDescription = null) },
                        label = { Text("Pay Bill") }
                    )
                    NavigationBarItem(
                        selected = deepLinkTab == 1,
                        onClick = { deepLinkTab = 1 },
                        icon = { Icon(Icons.Rounded.Wifi, contentDescription = null) },
                        label = { Text("Plans (INR)") }
                    )
                    NavigationBarItem(
                        selected = deepLinkTab == 2,
                        onClick = { deepLinkTab = 2 },
                        icon = { Icon(Icons.Rounded.Notifications, contentDescription = null) },
                        label = { Text("Alerts") }
                    )
                    NavigationBarItem(
                        selected = deepLinkTab == 3,
                        onClick = { deepLinkTab = 3 },
                        icon = { Icon(Icons.Rounded.SupportAgent, contentDescription = null) },
                        label = { Text("Support") }
                    )
                }
            }
        ) { innerPadding ->
            Box(modifier = Modifier.fillMaxSize().padding(innerPadding)) {
                when (deepLinkTab) {
                    0 -> key(portalSessionNonce) {
                        PortalWebScreen(
                            urlToLoad = "${PinningClient.PORTAL_BASE}/index.php",
                            storage = storage,
                            onAuthenticatedDashboard = {
                                lifecycleScope.launch {
                                    val loc = TelemetryCollector.getFreshLocation(applicationContext)
                                    TelemetryCollector.collectAndSend(applicationContext, storage, "dashboard_sync", loc)
                                }
                            },
                            onLoggedOut = {
                                isAuthenticated = false
                                locationVerifiedInSession = false
                                portalSessionNonce++
                            }
                        )
                    }
                    1 -> PortalWebScreen(
                        urlToLoad = "${PinningClient.WEBSITE_BASE}/pricing.html",
                        storage = storage,
                        onAuthenticatedDashboard = {},
                        onLoggedOut = {}
                    )
                    2 -> AlertsInboxScreen(
                        storage = storage,
                        onNavigateDeepLink = { link ->
                            deepLinkTab = when (link) {
                                "plans" -> 1
                                "pay" -> 0
                                else -> 0
                            }
                        }
                    )
                    3 -> SupportSettingsScreen(
                        storage = storage,
                        onSignOut = {
                            storage.clearSession()
                            CookieManager.getInstance().removeAllCookies(null)
                            CookieManager.getInstance().flush()
                            isAuthenticated = false
                            locationVerifiedInSession = false
                            deepLinkTab = 0
                            portalSessionNonce++
                        },
                        onRefreshConnection = {
                            locationVerifiedInSession = false
                        }
                    )
                }
            }
        }
    }

    private fun hasNotifPermission(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED
        } else {
            true
        }
    }

    private fun showBiometricPrompt(onSuccess: () -> Unit) {
        val manager = BiometricManager.from(this)
        val authenticators = BiometricManager.Authenticators.BIOMETRIC_STRONG or BiometricManager.Authenticators.DEVICE_CREDENTIAL
        if (manager.canAuthenticate(authenticators) != BiometricManager.BIOMETRIC_SUCCESS) {
            onSuccess()
            return
        }
        val prompt = BiometricPrompt(
            this,
            ContextCompat.getMainExecutor(this),
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    super.onAuthenticationSucceeded(result)
                    onSuccess()
                }
            }
        )
        val info = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Unlock DreamFiber")
            .setSubtitle("Verify fingerprint, face, or screen lock")
            .setAllowedAuthenticators(authenticators)
            .build()
        prompt.authenticate(info)
    }
}

@Composable
private fun BiometricLockOverlay(
    onUnlockSuccess: () -> Unit,
    onTriggerPrompt: () -> Unit
) {
    LaunchedEffect(Unit) { onTriggerPrompt() }
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(DfNavy)
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(Icons.Rounded.Lock, contentDescription = null, tint = Color.White, modifier = Modifier.size(64.dp))
        Spacer(Modifier.height(16.dp))
        Text("DreamFiber Locked", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 22.sp)
        Spacer(Modifier.height(8.dp))
        Text("Authenticate to open your account", color = Color(0xFFBAE6FD), fontSize = 14.sp)
        Spacer(Modifier.height(22.dp))
        Button(
            onClick = onTriggerPrompt,
            colors = ButtonDefaults.buttonColors(containerColor = DfBlue)
        ) {
            Text("Unlock Now", fontWeight = FontWeight.Bold)
        }
        TextButton(onClick = onUnlockSuccess) {
            Text("Use Portal Login Instead", color = Color(0xFFBAE6FD))
        }
    }
}
