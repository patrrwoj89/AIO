import os

project_name = "NeoTV"
pkg = "com.polskitv.ultimate"
pkg_path = pkg.replace(".", "/")
base_java = f"{project_name}/app/src/main/java/{pkg_path}"

# 1. PEŁNA LISTA FOLDERÓW (Struktura profesjonalnego projektu)
folders = [
    f"{project_name}/gradle/wrapper",
    f"{project_name}/app/libs",
    f"{project_name}/app/src/main/res/values",
    f"{project_name}/app/src/main/res/drawable",
    f"{base_java}/data/model",
    f"{base_java}/data/repository",
    f"{base_java}/data/scraper",
    f"{base_java}/ui/screens",
    f"{base_java}/ui/theme"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 2. DEFINICJA WSZYSTKICH PLIKÓW (Konfiguracja + Kod)
files = {
    # --- ROOT CONFIG ---
    f"{project_name}/settings.gradle.kts": f"""
rootProject.name = "{project_name}"
include(":app")
""",
    f"{project_name}/build.gradle.kts": """
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.0" apply false
}
""",
    f"{project_name}/gradle.properties": "android.useAndroidX=true\nkotlin.code.style=official",

    # --- APP CONFIG ---
    f"{project_name}/app/build.gradle.kts": f"""
plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{pkg}"
    compileSdk = 34

    defaultConfig {{
        applicationId = "{pkg}"
        minSdk = 23
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }}

    buildFeatures {{ compose = true }}
    composeOptions {{ kotlinCompilerExtensionVersion = "1.5.1" }}
    
    packaging {{
        resources {{
            excludes += "/META-INF/{{AL2.0,LGPL2.1}}"
        }}
    }}
}}

dependencies {{
    implementation("androidx.tv:tv-foundation:1.0.0-alpha10")
    implementation("androidx.tv:tv-material:1.0.0-alpha10")
    implementation("androidx.media3:media3-exoplayer:1.2.0")
    implementation("androidx.media3:media3-ui:1.2.0")
    implementation("io.ktor:ktor-client-android:2.3.5")
    implementation("org.jsoup:jsoup:1.17.2")
    implementation("io.coil-kt:coil-compose:2.5.0")
    implementation(fileTree(mapOf("dir" to "libs", "include" to listOf("*.aar"))))
}}
""",

    # --- MANIFEST ---
    f"{project_name}/app/src/main/AndroidManifest.xml": f"""
<manifest xmlns:android="http://android.com">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-feature android:name="android.software.leanback" android:required="false" />
    <application
        android:label="NeoTV Ultimate"
        android:theme="@style/Theme.AppCompat.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""",

    # --- KOD KOTLIN (MAIN) ---
    f"{base_java}/MainActivity.kt": f"""
package {pkg}
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.polskitv.ultimate.ui.screens.DashboardScreen
import com.stremio.core.Core
import com.stremio.core.runtime.AndroidEnv
import com.stremio.core.storage.AndroidStorage

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        try {{
            Core(AndroidStorage(this), AndroidEnv(this))
        }} catch (e: Exception) {{ e.printStackTrace() }}
        
        setContent {{ DashboardScreen() }}
    }}
}}
""",

    # --- SILNIK AUTONAPRAWY ---
    f"{base_java}/data/scraper/SmartScraper.kt": f"""
package {pkg}.data.scraper
import org.jsoup.Jsoup
import kotlinx.coroutines.*

class SmartScraper {{
    suspend fun search(query: String) = coroutineScope {{
        async(Dispatchers.IO) {{
            try {{
                val doc = Jsoup.connect("https://cda.pl" + query).get()
                doc.select("a").filter {{ it.text().contains(query, true) }}
            } catch (e: Exception) {{ emptyList() }}
        }}
    }}
}}
""",

    # --- UI DASHBOARD ---
    f"{base_java}/ui/screens/DashboardScreen.kt": f"""
package {pkg}.ui.screens
import androidx.compose.runtime.*
import androidx.tv.material3.*
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier

@OptIn(ExperimentalTvMaterial3Api::class)
@Composable
fun DashboardScreen() {{
    Box(modifier = Modifier.fillMaxSize()) {{
        Text("NeoTV Ultimate Gotowy!", style = MaterialTheme.typography.displayLarge)
    }}
}}
""",

    # --- SCRAPERS JSON ---
    f"{project_name}/scrapers.json": """
[
  {"name":"CDA","searchUrl":"https://cda.pl{q}","itemSelector":"div.elem-video","titleSelector":"a.link-title","linkSelector":"a.link-title"},
  {"name":"Filman","searchUrl":"https://filman.cc{q}","itemSelector":"div.item","titleSelector":"h2","linkSelector":"a"}
]
"""
}

# 3. ZAPISYWANIE PLIKÓW
print(f"🚀 Generuję kompletny projekt w folderze: {os.path.abspath(project_name)}")
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print("\n✅ GOTOWE!")
print(f"1. Wklej 'stremio-core-kotlin.aar' do folderu: {project_name}/app/libs")
print(f"2. Otwórz folder '{project_name}' w Android Studio (File -> Open).")
print(f"3. Czekaj na 'Gradle Sync' na dole ekranu.")
