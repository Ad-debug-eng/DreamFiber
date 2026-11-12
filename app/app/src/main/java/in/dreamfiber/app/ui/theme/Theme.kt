package `in`.dreamfiber.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val DfNavy = Color(0xFF002B5E)
val DfBlue = Color(0xFF0072F0)
val DfSky = Color(0xFF38BDF8)
val DfGreen = Color(0xFF16A34A)
val DfAmber = Color(0xFFD97706)
val DfRed = Color(0xFFDC2626)

private val LightColors = lightColorScheme(
    primary = DfBlue,
    onPrimary = Color.White,
    secondary = DfNavy,
    onSecondary = Color.White,
    tertiary = DfSky,
    background = Color(0xFFF8FAFC),
    surface = Color.White,
    onBackground = Color(0xFF0F172A),
    onSurface = Color(0xFF0F172A),
    surfaceVariant = Color(0xFFE2E8F0)
)

private val DarkColors = darkColorScheme(
    primary = DfSky,
    onPrimary = Color(0xFF001E3C),
    secondary = DfBlue,
    onSecondary = Color.White,
    background = Color(0xFF0F172A),
    surface = Color(0xFF1E293B),
    onBackground = Color(0xFFF8FAFC),
    onSurface = Color(0xFFF8FAFC),
    surfaceVariant = Color(0xFF334155)
)

@Composable
fun DreamFiberTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content
    )
}
