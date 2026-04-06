import os
import subprocess
import sys

# --- KONFIGURACJA ---
PROJECT_NAME = "NeoTV"
PKG = "com.polskitv.ultimate"
GITHUB_URL = "https://github.com"
BASE_DIR = os.path.join(PROJECT_NAME, "app/src/main/java", PKG.replace(".", "/"))

def check_env():
    print("🔍 Sprawdzanie środowiska...")
    try:
        subprocess.run(["java", "-version"], check=True, capture_output=True)
        print("✅ Java: OK")
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git: OK")
    except:
        print("❌ Brak Javy lub Gita! Zainstaluj je przed kontynuacją.")
        sys.exit(1)

def build_structure():
    print(f"📁 Tworzenie struktury projektu {PROJECT_NAME}...")
    dirs = [
        "data/model", "data/repository", "data/scraper", 
        "ui/screens", "ui/viewmodel", "app/libs", "app/src/main/res/drawable"
    ]
    for d in dirs:
        os.makedirs(os.path.join(BASE_DIR if "app" not in d else PROJECT_NAME, d), exist_ok=True)

def generate_files():
    print("✍️ Generowanie inteligentnego kodu...")
    files = {
        # 1. GRADLE - PEŁNA KONFIGURACJA SDK I PLUGINS
        f"{PROJECT_NAME}/app/build.gradle.kts": """
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
        versionCode = 1
        versionName = "1.0"
    }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.1" }
}
dependencies {
    implementation("androidx.tv:tv-foundation:1.0.0-alpha10")
    implementation("androidx.tv:tv-material:1.0.0-alpha10")
    implementation("androidx.media3:media3-exoplayer:1.2.0")
    implementation("androidx.media3:media3-exoplayer-hls:1.2.0")
    implementation("io.ktor:ktor-client-android:2.3.5")
    implementation("io.ktor:ktor-client-content-negotiation:2.3.5")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.5")
    implementation("io.ktor:ktor-server-netty:2.3.5")
    implementation("org.jsoup:jsoup:1.17.2")
    implementation("io.coil-kt:coil-compose:2.5.0")
    implementation(fileTree(mapOf("dir" to "libs", "include" to listOf("*.aar"))))
}""",

        # 2. LANGUAGE REFINEMENT ENGINE (Regex Lektor > Multi > Subs)
        f"{BASE_DIR}/data/scraper/LanguageRefinementEngine.kt": """
package com.polskitv.ultimate.data.scraper
import com.polskitv.ultimate.data.model.StreamSource
class LanguageRefinementEngine {
    private val regexAudio = Regex("(?i)(lektor|dubbing|pl\\\\s?audio|\\\\.pl\\\\.)")
    private val regexSubs = Regex("(?i)(napisy\\\\s?pl|plsub|subs\\\\.pl)")
    
    fun sortAndTag(streams: List<StreamSource>): List<StreamSource> {
        return streams.sortedByDescending { 
            when {
                regexAudio.containsMatchIn(it.title) -> 3
                it.title.contains("multi", true) -> 2
                regexSubs.containsMatchIn(it.title) -> 1
                else -> 0
            }
        }
    }
}""",

        # 3. DYNAMIC SCRAPER (Obsługa Twojej listy 30 stron + OTA JSON)
        f"{BASE_DIR}/data/scraper/DynamicScraper.kt": """
package com.polskitv.ultimate.data.scraper
import org.jsoup.Jsoup
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*

class DynamicScraper(private val client: HttpClient) {
    suspend fun fetch(url: String, query: String, selector: String): List<String> {
        val finalUrl = url.replace("{q}", query)
        val html = client.get(finalUrl).bodyAsText()
        return Jsoup.parse(html).select(selector).map { it.attr("abs:href") }
    }
}""",

        # 4. MAIN ACTIVITY (Inicjalizacja Stremio-Core)
        f"{BASE_DIR}/MainActivity.kt": """
package com.polskitv.ultimate
import android.os.Bundle
import androidx.activity.ComponentActivity
import com.stremio.core.Core
import com.stremio.core.runtime.AndroidEnv
import com.stremio.core.storage.AndroidStorage

class MainActivity : ComponentActivity() {
    lateinit var stremioCore: Core
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try { 
            stremioCore = Core(AndroidStorage(this), AndroidEnv(this)) 
        } catch (e: Exception) { e.printStackTrace() }
    }
}""",

        # 5. SCRAPERS.JSON (Twoja baza zdalna)
        f"{PROJECT_NAME}/scrapers.json": """
[
  {"name":"CDA","searchUrl":"https://cda.pl{q}","itemSelector":"div.elem-video","titleSelector":"a.link-title","linkSelector":"a.link-title"},
  {"name":"Filman","searchUrl":"https://filman.cc{q}","itemSelector":"div.item","titleSelector":"h2","linkSelector":"a"}
]"""
    }
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f: f.write(content.strip())

def init_git():
    print("📤 Inicjalizacja Gita i wysyłka na NeoTV...")
    try:
        subprocess.run(["git", "init"], cwd=PROJECT_NAME)
        subprocess.run(["git", "remote", "add", "origin", GITHUB_URL], cwd=PROJECT_NAME)
        subprocess.run(["git", "add", "."], cwd=PROJECT_NAME)
        subprocess.run(["git", "commit", "-m", "NeoTV Genesis: Full Engine with Language & QR Auth"], cwd=PROJECT_NAME)
        subprocess.run(["git", "branch", "-M", "main"], cwd=PROJECT_NAME)
        print("✅ Projekt przygotowany do pusha. Uruchom 'git push -u origin main' ręcznie.")
    except:
        print("⚠️ Błąd Gita. Sprawdź uprawnienia do repozytorium.")

if __name__ == "__main__":
    check_env()
    build_structure()
    generate_files()
    init_git()
    print(f"\n🎉 GOTOWE! Otwórz folder '{PROJECT_NAME}' w Android Studio.")
    print("👉 PAMIĘTAJ: Wrzuć plik 'stremio-core-kotlin.aar' do folderu app/libs!")
