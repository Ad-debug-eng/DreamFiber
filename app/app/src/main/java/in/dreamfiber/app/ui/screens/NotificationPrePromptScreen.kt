package `in`.dreamfiber.app.ui.screens

import android.Manifest
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Alarm
import androidx.compose.material.icons.rounded.Celebration
import androidx.compose.material.icons.rounded.NotificationsActive
import androidx.compose.material.icons.rounded.Wifi
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import `in`.dreamfiber.app.security.SecureStorage
import `in`.dreamfiber.app.ui.theme.DfBlue
import `in`.dreamfiber.app.ui.theme.DfNavy

/**
 * Friendly pre-permission explanation shown BEFORE Android 13+'s system POST_NOTIFICATIONS popup.
 * Increases customer opt-in rates for recharge expiry reminders and festival/offer image alerts.
 */
@Composable
fun NotificationPrePromptScreen(
    storage: SecureStorage,
    onDone: () -> Unit
) {
    val notifLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) {
        storage.notifPrePromptShown = true
        onDone()
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(DfNavy, Color(0xFF0F172A))))
            .padding(24.dp),
        contentAlignment = Alignment.Center
    ) {
        Card(
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(26.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Box(
                    modifier = Modifier
                        .size(72.dp)
                        .clip(CircleShape)
                        .background(Brush.linearGradient(listOf(DfNavy, DfBlue))),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Rounded.NotificationsActive,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(36.dp)
                    )
                }

                Spacer(Modifier.height(16.dp))

                Text(
                    text = "Never Miss a Recharge or Offer",
                    style = MaterialTheme.typography.headlineSmall.copy(fontWeight = FontWeight.ExtraBold),
                    textAlign = TextAlign.Center
                )

                Spacer(Modifier.height(8.dp))

                Text(
                    text = "Turn on DreamFiber notifications so you receive:",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                    ),
                    textAlign = TextAlign.Center
                )

                Spacer(Modifier.height(18.dp))

                BenefitRow(Icons.Rounded.Alarm, "Timely Expiry Reminders", "Polite daytime alerts before & after your plan expires — cancelled automatically once you renew.")
                Spacer(Modifier.height(12.dp))
                BenefitRow(Icons.Rounded.Celebration, "Festivals & Special Offers", "Seasonal bonus validity, OTT bundles, and festival greetings.")
                Spacer(Modifier.height(12.dp))
                BenefitRow(Icons.Rounded.Wifi, "Service & Maintenance Updates", "Proactive fiber maintenance notices in your area.")

                Spacer(Modifier.height(24.dp))

                Button(
                    onClick = {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                            notifLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
                        } else {
                            storage.notifPrePromptShown = true
                            onDone()
                        }
                    },
                    shape = RoundedCornerShape(14.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = DfBlue),
                    modifier = Modifier.fillMaxWidth().height(52.dp)
                ) {
                    Text("Allow Notifications", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                }

                Spacer(Modifier.height(8.dp))

                TextButton(
                    onClick = {
                        storage.notifPrePromptShown = true
                        onDone()
                    }
                ) {
                    Text("Not Now", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.65f))
                }
            }
        }
    }
}

@Composable
private fun BenefitRow(icon: ImageVector, title: String, desc: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(DfBlue.copy(alpha = 0.06f))
            .padding(12.dp),
        verticalAlignment = Alignment.Top
    ) {
        Icon(icon, contentDescription = null, tint = DfBlue, modifier = Modifier.size(22.dp))
        Spacer(Modifier.width(12.dp))
        Column {
            Text(title, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Spacer(Modifier.height(2.dp))
            Text(desc, fontSize = 12.5.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f))
        }
    }
}
