# Analizador de Textos Avanzado - Script de ejecución
# Autor: Christian Lera

# Configurar política de ejecución solo para esta sesión
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Colores para la consola
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Cyan"
Clear-Host

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   ANALIZADOR DE TEXTOS AVANZADO" -ForegroundColor Yellow
Write-Host "   Autor: Christian Lera" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[INFO] Verificando Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "[SOLUCION] Instala Python desde https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "           Asegurate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host ""

# Verificar dependencias
Write-Host "[INFO] Verificando dependencias..." -ForegroundColor Cyan
$missingDeps = @()

try {
    $matplotlib = python -c "import matplotlib" 2>&1
} catch {
    $missingDeps += "matplotlib"
}

try {
    $langdetect = python -c "import langdetect" 2>&1
} catch {
    $missingDeps += "langdetect"
}

try {
    $textblob = python -c "import textblob" 2>&1
} catch {
    $missingDeps += "textblob"
}

try {
    $numpy = python -c "import numpy" 2>&1
} catch {
    $missingDeps += "numpy"
}

if ($missingDeps.Count -gt 0) {
    Write-Host "[ADVERTENCIA] Dependencias faltantes: $($missingDeps -join ', ')" -ForegroundColor Yellow
    Write-Host "[INFO] Instalando dependencias..." -ForegroundColor Cyan
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Error al instalar dependencias" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    Write-Host "[OK] Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "[OK] Todas las dependencias verificadas" -ForegroundColor Green
}
Write-Host ""

# Ejecutar aplicación
Write-Host "[INFO] Iniciando aplicación..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

try {
    python ContadorDePalabras.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[INFO] Aplicación cerrada correctamente" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[ERROR] La aplicación se cerró con código de error: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] Error al ejecutar la aplicación: $_" -ForegroundColor Red
    Write-Host "[INFO] Verifica que el archivo ContadorDePalabras.py exista en el directorio actual" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Presiona Enter para salir"