# Script de instalación de dependencias - Analizador de Textos Avanzado
# Autor: Christian Lera
# Uso: Ejecutar como Administrador (recomendado) o usuario normal

param(
    [switch]$Upgrade,
    [switch]$Force
)

# Configurar colores y consola
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Cyan"
Clear-Host

# Función para escribir con color
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Banner
Write-ColorOutput "================================================" "Cyan"
Write-ColorOutput "   INSTALADOR DE DEPENDENCIAS" "Yellow"
Write-ColorOutput "   Analizador de Textos Avanzado" "White"
Write-ColorOutput "   Autor: Christian Lera" "Gray"
Write-ColorOutput "================================================" "Cyan"
Write-ColorOutput ""

# Verificar si Python está instalado
Write-ColorOutput "[1/5] Verificando Python..." "Cyan"
try {
    $pythonVersion = python --version 2>&1
    Write-ColorOutput "      ✓ $pythonVersion" "Green"
} catch {
    Write-ColorOutput "      ✗ Python no encontrado" "Red"
    Write-ColorOutput ""
    Write-ColorOutput "ERROR: Python no está instalado o no está en el PATH" "Red"
    Write-ColorOutput "SOLUCIÓN: Descarga Python desde https://www.python.org/downloads/" "Yellow"
    Write-ColorOutput "          Asegurate de marcar 'Add Python to PATH' durante la instalación" "Yellow"
    Write-ColorOutput ""
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-ColorOutput ""

# Verificar pip
Write-ColorOutput "[2/5] Verificando pip..." "Cyan"
try {
    $pipVersion = pip --version 2>&1
    Write-ColorOutput "      ✓ pip instalado" "Green"
} catch {
    Write-ColorOutput "      ✗ pip no encontrado" "Red"
    Write-ColorOutput ""
    Write-ColorOutput "ERROR: pip no está instalado" "Red"
    Write-ColorOutput "SOLUCIÓN: python -m ensurepip --upgrade" "Yellow"
    Write-ColorOutput ""
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-ColorOutput ""

# Actualizar pip
Write-ColorOutput "[3/5] Actualizando pip..." "Cyan"
try {
    python -m pip install --upgrade pip
    Write-ColorOutput "      ✓ pip actualizado" "Green"
} catch {
    Write-ColorOutput "      ⚠ No se pudo actualizar pip (continuando...)" "Yellow"
}
Write-ColorOutput ""

# Lista de dependencias
$dependencies = @(
    "matplotlib>=3.5.0",
    "langdetect>=1.0.9",
    "textblob>=0.17.1",
    "numpy>=1.21.0"
)

# Instalar dependencias
Write-ColorOutput "[4/5] Instalando dependencias..." "Cyan"
Write-ColorOutput "      Dependencias a instalar:" "Gray"
foreach ($dep in $dependencies) {
    Write-ColorOutput "        - $dep" "Gray"
}
Write-ColorOutput ""

$installSuccess = @()
$installFailed = @()

foreach ($dep in $dependencies) {
    $depName = ($dep -split ">=")[0]
    Write-ColorOutput "      Instalando $depName..." "White"
    
    $installCmd = "pip install $dep"
    if ($Upgrade) {
        $installCmd += " --upgrade"
    }
    if ($Force) {
        $installCmd += " --force-reinstall --no-cache-dir"
    }
    
    try {
        Invoke-Expression $installCmd 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "        ✓ $depName instalado correctamente" "Green"
            $installSuccess += $depName
        } else {
            Write-ColorOutput "        ✗ Error al instalar $depName" "Red"
            $installFailed += $depName
        }
    } catch {
        Write-ColorOutput "        ✗ Excepción al instalar $depName" "Red"
        $installFailed += $depName
    }
}
Write-ColorOutput ""

# Descargar datos de TextBlob (necesario para análisis de sentimiento)
Write-ColorOutput "[5/5] Configurando TextBlob..." "Cyan"
try {
    python -c "import textblob; from textblob import download_corpora; download_corpora()" 2>&1 | Out-Null
    Write-ColorOutput "      ✓ Corpus de TextBlob descargado" "Green"
} catch {
    Write-ColorOutput "      ⚠ No se pudieron descargar los corpus de TextBlob" "Yellow"
    Write-ColorOutput "        Ejecuta manualmente: python -c 'import textblob; textblob.download_corpora()'" "Gray"
}
Write-ColorOutput ""

# Resumen final
Write-ColorOutput "================================================" "Cyan"
Write-ColorOutput "   RESUMEN DE INSTALACIÓN" "Yellow"
Write-ColorOutput "================================================" "Cyan"

if ($installSuccess.Count -gt 0) {
    Write-ColorOutput "  ✓ Instalados correctamente: $($installSuccess -join ', ')" "Green"
}
if ($installFailed.Count -gt 0) {
    Write-ColorOutput "  ✗ Fallaron: $($installFailed -join ', ')" "Red"
}

Write-ColorOutput ""
Write-ColorOutput "  Total: $($installSuccess.Count)/$($dependencies.Count) dependencias instaladas" "Cyan"
Write-ColorOutput ""

if ($installFailed.Count -eq 0) {
    Write-ColorOutput "✅ INSTALACIÓN COMPLETA" "Green"
    Write-ColorOutput "   Puedes ejecutar la aplicación con: .\ejecutar.ps1" "White"
} else {
    Write-ColorOutput "⚠ INSTALACIÓN INCOMPLETA" "Yellow"
    Write-ColorOutput "   Revisa los errores arriba o instala manualmente:" "Yellow"
    Write-ColorOutput "   pip install matplotlib langdetect textblob numpy" "Gray"
}

Write-ColorOutput ""
Read-Host "Presiona Enter para salir"