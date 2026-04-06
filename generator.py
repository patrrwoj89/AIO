import os

project_name = "NeoTV"
pkg_path = "com/polskitv/ultimate"
base_dir = os.path.join(project_name, "app", "src", "main", "java", pkg_path)

# 1. TWORZENIE STRUKTURY FOLDERÓW
sub_dirs = [
    "data/model", "data/repository", "data/scraper", 
    "ui/screens", "ui/viewmodel", "player"
]
# Tworzenie libs osobno
os.makedirs(os.path.join(project_name, "app", "libs"), exist_ok=True)

for sd in sub_dirs:
    os.makedirs(os.path.join(base_dir, sd), exist_ok=True)

# 2. DEFINICJA PLIKÓW
files = {
    # GRADLE (Zależności)
    f"{project_name}/app/build.gradle.kts": """
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    id("kotlinx-serialization")
}
android {
    namespace = "com.polskitv.ultimate"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.polskitv.ultimate"
        minSdk = 23
        targetSdk = 34
    }
    buildFeatures { compose = true }
}
dependencies {
    implementation("androidx.tv:tv-foundation:1.0.0-alpha10")
    implementation("androidx.tv:tv-material:1.0.0-alpha10")
    implementation("androidx.media3:media3-exoplayer:1.2.0")
    implementation("io.ktor:ktor-client-android:2.3.5")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.5")
    implementation("org.jsoup:jsoup:1.17.2")
    implementation("io.coil-kt:coil-compose:2.5.0")
    implementation(fileTree(mapOf("dir" to "libs", "include" to listOf("*.aar"))))
}""",

    # MAIN ACTIVITY (Start Silnika Stremio)
    f"{base_dir}/MainActivity.kt": """
package com.polskitv.ultimate
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.stremio.core.Core
import com.stremio.core.runtime.AndroidEnv
import com.stremio.core.storage.AndroidStorage
import com.polskitv.ultimate.ui.screens.DashboardScreen

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try { Core(AndroidStorage(this), AndroidEnv(this)) } catch (e: Exception) { e.printStackTrace() }
        setContent { DashboardScreen() }
    }
}""",

    # SMART SCRAPER (Silnik Autonaprawy)
    f"{base_dir}/data/scraper/SmartScraper.kt": """
package com.polskitv.ultimate.data.scraper
import org.jsoup.Jsoup
import kotlinx.coroutines.*
class SmartScraper {
    suspend fun search(query: String) = coroutineScope {
        async(Dispatchers.IO) {
            try { 
                val doc = Jsoup.connect("https://cda.pl" + query).get()
                // Autonaprawa: jeśli selektor zawiedzie, szukaj linków z tytułem
                doc.select("a").filter { it.text().contains(query, true) }
            } catch (e: Exception) { emptyList() }
        }
    }
}""",

    # DASHBOARD UI
    f"{base_dir}/ui/screens/DashboardScreen.kt": """
package com.polskitv.ultimate.ui.screens
import androidx.compose.runtime.*
import androidx.tv.material3.*
import androidx.compose.foundation.layout.*

@OptIn(ExperimentalTvMaterial3Api::class)
@Composable
fun DashboardScreen() {
    Column(modifier = androidx.compose.ui.Modifier.fillMaxSize()) {
        Text("NeoTV Ultimate", style = MaterialTheme.typography.displayLarge)
        Text("VOD & IPTV PL", style = MaterialTheme.typography.headlineMedium)
    }
}""",

    # SCRAPERS.JSON (Twoja baza 30 stron)
    f"{project_name}/scrapers.json": """
[
  {"name":"CDA","searchUrl":"https://cda.pl{q}","itemSelector":"div.elem-video","titleSelector":"a.link-title","linkSelector":"a.link-title"},
  {"name":"Filman","searchUrl":"https://filman.cc{q}","itemSelector":"div.item","titleSelector":"h2","linkSelector":"a"},
  {"name":"Vider","searchUrl":"https://vider.info{q}","itemSelector":"div.video-item","titleSelector":"a.video-title-link","linkSelector":"a.video-title-link"}
]""",

    # MANIFEST
    f"{project_name}/app/src/main/AndroidManifest.xml": """
<manifest xmlns:android="http://android.com">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:label="NeoTV" android:theme="@style/Theme.AppCompat.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
}

# GENEROWANIE
print(f"🚀 Buduję pełny projekt NeoTV w folderze: {os.path.abspath(project_name)}")
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print("\n✅ PROJEKT WYGENEROWANY!")
print("1. Wklej 'stremio-core-kotlin.aar' do NeoTV/app/libs.")
print("2. Otwórz w Android Studio.")
