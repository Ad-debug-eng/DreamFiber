package `in`.dreamfiber.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.NotificationsNone
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import `in`.dreamfiber.app.security.InboxNotification
import `in`.dreamfiber.app.security.PinningClient
import `in`.dreamfiber.app.security.SecureStorage
import `in`.dreamfiber.app.ui.theme.DfAmber
import `in`.dreamfiber.app.ui.theme.DfBlue
import `in`.dreamfiber.app.ui.theme.DfGreen
import `in`.dreamfiber.app.ui.theme.DfNavy
import kotlinx.coroutines.launch

@Composable
fun AlertsInboxScreen(
    storage: SecureStorage,
    onNavigateDeepLink: (String) -> Unit
) {
    val scope = rememberCoroutineScope()
    var notifications by remember { mutableStateOf<List<InboxNotification>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    fun reload() {
        isLoading = true
        scope.launch {
            notifications = PinningClient.fetchInbox(storage.username)
            isLoading = false
        }
    }

    LaunchedEffect(storage.username) {
        reload()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(DfNavy)
                .padding(horizontal = 18.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column {
                Text("Notifications & Offers", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                Text("Festivals, special offers & expiry reminders", color = Color(0xFFBAE6FD), fontSize = 12.sp)
            }
            IconButton(onClick = { reload() }) {
                Icon(Icons.Rounded.Refresh, contentDescription = "Refresh", tint = Color.White)
            }
        }

        if (isLoading) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = DfBlue)
            }
        } else if (notifications.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(
                        Icons.Rounded.NotificationsNone,
                        contentDescription = null,
                        modifier = Modifier.size(60.dp),
                        tint = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.4f)
                    )
                    Spacer(Modifier.height(10.dp))
                    Text("No alerts or offers yet", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Spacer(Modifier.height(4.dp))
                    Text(
                        "Festival greetings, broadband offers, and recharge reminders will appear here.",
                        fontSize = 13.sp,
                        color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.65f)
                    )
                }
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                items(notifications, key = { it.id }) { item ->
                    AlertCard(item = item, onAction = { onNavigateDeepLink(item.deepLink) })
                }
            }
        }
    }
}

@Composable
private fun AlertCard(
    item: InboxNotification,
    onAction: () -> Unit
) {
    val badgeColor = when (item.campaignType) {
        "festival" -> Color(0xFF9333EA)
        "expiry_auto" -> DfAmber
        "offer" -> DfGreen
        else -> DfBlue
    }
    val badgeLabel = when (item.campaignType) {
        "festival" -> "Festival"
        "expiry_auto" -> "Expiry Alert"
        "offer" -> "Special Offer"
        "outage" -> "Service Update"
        else -> "Announcement"
    }

    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 3.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column {
            if (item.imageUrl.startsWith("https://")) {
                AsyncImage(
                    model = item.imageUrl,
                    contentDescription = item.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(165.dp)
                        .clip(RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp))
                )
            }
            Column(Modifier.padding(16.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Surface(
                        color = badgeColor.copy(alpha = 0.14f),
                        shape = RoundedCornerShape(50)
                    ) {
                        Text(
                            text = badgeLabel,
                            color = badgeColor,
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                        )
                    }
                    Text(
                        text = item.createdAt.take(10),
                        fontSize = 11.5.sp,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.55f)
                    )
                }
                Spacer(Modifier.height(8.dp))
                Text(item.title, fontWeight = FontWeight.ExtraBold, fontSize = 16.sp)
                Spacer(Modifier.height(4.dp))
                Text(
                    item.body,
                    fontSize = 13.5.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.78f)
                )
                if (item.deepLink in listOf("pay", "plans")) {
                    Spacer(Modifier.height(10.dp))
                    Button(
                        onClick = onAction,
                        shape = RoundedCornerShape(10.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = DfBlue),
                        contentPadding = PaddingValues(horizontal = 14.dp, vertical = 6.dp)
                    ) {
                        Text(
                            if (item.deepLink == "pay") "Pay Bill Now" else "View Plans (INR)",
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
    }
}
