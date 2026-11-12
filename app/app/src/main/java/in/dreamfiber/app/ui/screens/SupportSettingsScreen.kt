package `in`.dreamfiber.app.ui.screens

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.rounded.Logout
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import `in`.dreamfiber.app.security.PinningClient
import `in`.dreamfiber.app.security.SecureStorage
import `in`.dreamfiber.app.ui.theme.DfAmber
import `in`.dreamfiber.app.ui.theme.DfBlue
import `in`.dreamfiber.app.ui.theme.DfGreen
import `in`.dreamfiber.app.ui.theme.DfNavy
import `in`.dreamfiber.app.ui.theme.DfRed
import kotlinx.coroutines.launch

@Composable
fun SupportSettingsScreen(
    storage: SecureStorage,
    onSignOut: () -> Unit,
    onRefreshConnection: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var bioEnabled by remember { mutableStateOf(storage.biometricLockEnabled) }
    var privacyExpanded by remember { mutableStateOf(false) }
    var showDeleteDialog by remember { mutableStateOf(false) }
    var delMobile by remember { mutableStateOf("") }
    var delReason by remember { mutableStateOf("") }
    var delStatus by remember { mutableStateOf<String?>(null) }
    var isSubmittingDel by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .verticalScroll(rememberScrollState())
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(DfNavy)
                .padding(horizontal = 18.dp, vertical = 16.dp)
        ) {
            Text("Support & Settings", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 19.sp)
            Text(
                text = if (storage.username.isNotBlank()) "Signed in as ${storage.username}" else "DreamFiber Customer Care",
                color = Color(0xFFBAE6FD),
                fontSize = 12.5.sp
            )
        }

        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {

            // 1. Live ISP & Connection Verification Card
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Connection Status", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                        Surface(
                            color = if (storage.isOnDreamFiberNet) DfGreen.copy(alpha = 0.14f) else DfAmber.copy(alpha = 0.14f),
                            shape = RoundedCornerShape(50)
                        ) {
                            Text(
                                text = if (storage.isOnDreamFiberNet) "On DreamFiber Network" else "External Network",
                                color = if (storage.isOnDreamFiberNet) DfGreen else DfAmber,
                                fontSize = 11.5.sp,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                            )
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    Text("ISP: ${storage.lastIsp.ifBlank { "Checking..." }}", fontSize = 13.sp)
                    Text("Public IP: ${storage.lastIp.ifBlank { "-" }}", fontSize = 13.sp)
                    if (storage.lastCoords.isNotBlank()) {
                        Text("Verified Location: ${storage.lastCoords}", fontSize = 13.sp)
                    }
                    Spacer(Modifier.height(8.dp))
                    OutlinedButton(
                        onClick = onRefreshConnection,
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(Icons.Rounded.Refresh, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Re-Verify Connection & Speed", fontSize = 13.sp)
                    }
                }
            }

            // 2. App Security Card
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                        Icon(Icons.Rounded.Fingerprint, contentDescription = null, tint = DfBlue)
                        Spacer(Modifier.width(12.dp))
                        Column {
                            Text("Biometric App Lock", fontWeight = FontWeight.Bold, fontSize = 14.5.sp)
                            Text("Protect saved session with Fingerprint / Face", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.65f))
                        }
                    }
                    Switch(
                        checked = bioEnabled,
                        onCheckedChange = {
                            bioEnabled = it
                            storage.biometricLockEnabled = it
                        }
                    )
                }
            }

            // 3. Direct Customer Care Card
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(Modifier.padding(16.dp)) {
                    Text("Customer Care & Support", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    Spacer(Modifier.height(8.dp))
                    ActionRow(Icons.Rounded.Call, "Call Helpline: +91 92281 72558") {
                        context.startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:+919228172558")))
                    }
                    ActionRow(Icons.Rounded.Call, "Call Alternate: +91 87885 36698") {
                        context.startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:+918788536698")))
                    }
                    ActionRow(Icons.Rounded.Chat, "WhatsApp Support (+91 92721 62704)") {
                        openCustomTab(context, "https://wa.me/919272162704")
                    }
                    ActionRow(Icons.Rounded.Tv, "OTT Support (PlayBox: 022 4249 9955)") {
                        context.startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:02242499955")))
                    }
                }
            }

            // 4. Official Policies & Plans Links (Required for Payment Gateway & Play Store)
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(Modifier.padding(16.dp)) {
                    Text("Official Policies & Plans (INR)", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    Spacer(Modifier.height(6.dp))
                    ActionRow(Icons.Rounded.CurrencyRupee, "Plans & Pricing (INR)") {
                        openCustomTab(context, "${PinningClient.WEBSITE_BASE}/pricing.html")
                    }
                    ActionRow(Icons.Rounded.Description, "Terms & Conditions") {
                        openCustomTab(context, "${PinningClient.WEBSITE_BASE}/terms.html")
                    }
                    ActionRow(Icons.Rounded.ReceiptLong, "Refunds & Cancellations (5–7 business days)") {
                        openCustomTab(context, "${PinningClient.WEBSITE_BASE}/refunds.html")
                    }
                    ActionRow(Icons.Rounded.PrivacyTip, "Privacy Policy") {
                        openCustomTab(context, "${PinningClient.WEBSITE_BASE}/privacy.html")
                    }
                    ActionRow(Icons.Rounded.ContactSupport, "Contact Us") {
                        openCustomTab(context, "${PinningClient.WEBSITE_BASE}/contact.html")
                    }
                }
            }

            // 5. Sign Out
            OutlinedButton(
                onClick = onSignOut,
                shape = RoundedCornerShape(14.dp),
                modifier = Modifier.fillMaxWidth().height(48.dp)
            ) {
                Icon(Icons.AutoMirrored.Rounded.Logout, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Sign Out", fontWeight = FontWeight.Bold)
            }

            Spacer(Modifier.height(8.dp))

            // 6. Quiet / Tucked-Away Privacy & Account Data Section (not visible on home dashboard)
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 6.dp, bottom = 24.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { privacyExpanded = !privacyExpanded }
                        .padding(vertical = 8.dp, horizontal = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = "Privacy & Account Data Options",
                        fontSize = 12.5.sp,
                        color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.55f),
                        fontWeight = FontWeight.Medium
                    )
                    Icon(
                        imageVector = if (privacyExpanded) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.45f),
                        modifier = Modifier.size(18.dp)
                    )
                }

                AnimatedVisibility(visible = privacyExpanded) {
                    Card(
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.45f)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(Modifier.padding(14.dp)) {
                            Text(
                                "You can request deletion of your DreamFiber app profile, cached location logs, and push notification tokens at any time.",
                                fontSize = 12.sp,
                                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                            )
                            Spacer(Modifier.height(10.dp))
                            if (delStatus != null) {
                                Text(delStatus ?: "", fontSize = 12.5.sp, color = DfGreen, fontWeight = FontWeight.SemiBold)
                                Spacer(Modifier.height(8.dp))
                            }
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                TextButton(onClick = { showDeleteDialog = true }) {
                                    Text("Request App Data Deletion", color = DfRed, fontSize = 12.5.sp)
                                }
                                TextButton(onClick = { openCustomTab(context, "${PinningClient.WEBSITE_BASE}/delete-account.html") }) {
                                    Text("Web Deletion Form", fontSize = 12.5.sp)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (showDeleteDialog) {
        AlertDialog(
            onDismissRequest = { showDeleteDialog = false },
            title = { Text("Request Account & Data Deletion", fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text(
                        "This removes your app telemetry, location history, and push notification tokens. Statutory broadband KYC/billing records remain governed by DoT telecom laws.",
                        fontSize = 13.sp
                    )
                    Spacer(Modifier.height(10.dp))
                    OutlinedTextField(
                        value = delMobile,
                        onValueChange = { delMobile = it },
                        label = { Text("Registered Mobile Number") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(Modifier.height(8.dp))
                    OutlinedTextField(
                        value = delReason,
                        onValueChange = { delReason = it },
                        label = { Text("Reason (Optional)") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            },
            confirmButton = {
                Button(
                    enabled = !isSubmittingDel && (storage.username.isNotBlank() || delMobile.isNotBlank()),
                    colors = ButtonDefaults.buttonColors(containerColor = DfRed),
                    onClick = {
                        isSubmittingDel = true
                        scope.launch {
                            val (_, msg) = PinningClient.submitDeletionRequest(
                                username = storage.username,
                                mobile = delMobile,
                                reason = delReason.ifBlank { "Requested inside DreamFiber app" }
                            )
                            storage.wipeAllAppVault()
                            isSubmittingDel = false
                            showDeleteDialog = false
                            delStatus = msg
                        }
                    }
                ) {
                    Text(if (isSubmittingDel) "Submitting..." else "Confirm Deletion")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDeleteDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}

@Composable
private fun ActionRow(icon: ImageVector, label: String, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = DfBlue, modifier = Modifier.size(20.dp))
        Spacer(Modifier.width(12.dp))
        Text(label, fontSize = 13.5.sp, modifier = Modifier.weight(1f))
        Icon(Icons.AutoMirrored.Rounded.KeyboardArrowRight, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.45f))
    }
}

fun openCustomTab(context: Context, url: String) {
    try {
        CustomTabsIntent.Builder().setShowTitle(true).build().launchUrl(context, Uri.parse(url))
    } catch (_: Exception) {
        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    }
}
