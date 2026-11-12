# DreamFiber Release R8 / ProGuard Hardening Rules
-repackageclasses 'in.dreamfiber.o'
-allowaccessmodification
-optimizationpasses 5

# Preserve JS <-> Android WebView Bridge
-keepclassmembers class in.dreamfiber.app.ui.screens.PortalJsBridge {
    @android.webkit.JavascriptInterface <methods>;
}

# Preserve Firebase Messaging Service
-keep class in.dreamfiber.app.notifications.DreamFiberMessagingService { *; }

# Keep AndroidX Security Crypto / Tink classes
-keepclassmembers class * extends com.google.crypto.tink.shaded.protobuf.GeneratedMessageLite { *; }

# Strip debug logs in release APK
-assumenosideeffects class android.util.Log {
    public static int v(...);
    public static int d(...);
    public static int i(...);
}
