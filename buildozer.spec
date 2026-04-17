[app]
title = Nossa Conveniencia
package.name = nossaconv
package.domain = org.rafaeldrones
source.dir = .
# Adicionado 'json' e 'kv' que são comuns em apps Kivy
source.include_exts = py,png,jpg,json,kv
version = 1.0

# Requisitos corrigidos
# Adicionado 'hostpython3' para garantir a compilação no ambiente Linux
requirements = python3,hostpython3,kivy==2.3.0,requests,urllib3,chardet,idna,certifi

orientation = portrait
fullscreen = 0

# Configurações de Android
android.permissions = INTERNET
# API 33 é excelente para compatibilidade atual
android.api = 33
android.minapi = 21
android.ndk = 25b
# Deixe em branco para o buildozer baixar automaticamente no ambiente do GitHub
android.ndk_path = 
android.sdk_path = 

# Apenas arm64-v8a conforme solicitado
android.archs = arm64-v8a
android.allow_backup = True
# Isso ajuda a automatizar o aceite de licenças
android.accept_sdk_license = True

# Garante que o Gradle use o suporte a bibliotecas modernas
android.enable_androidx = True

[buildozer]
# Mantido em 2 para vermos detalhes se algo falhar novamente
log_level = 2
warn_on_root = 1