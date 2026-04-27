
# 🐍 AIRSIM PYTHON API — DOCUMENTACIÓN CLARA

AirSim expone una API en Python que funciona como **cliente remoto** del simulador.

👉 No controla el dron directamente
👉 Solo envía comandos por RPC al simulador

---

# 🧠 ARQUITECTURA PYTHON

```text id="pyarch"
Python script
    ↓ (RPC)
AirSim server (C++)
    ↓
Simulador (Unreal Engine)
```

---

# 📦 INSTALACIÓN (IMPORTANTE EN TU CASO)

## ✔ entorno recomendado

```bash id="pyenv"
python3.11 -m venv airsim-env
source airsim-env/bin/activate
```

---

## ✔ dependencias base

```bash id="pypack"
pip install numpy msgpack-rpc-python
pip install airsim
```

---

# 🚀 CONEXIÓN BÁSICA

```python id="connect"
import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
```

👉 Esto verifica que el simulador está activo.

---

# ✈️ CONTROL BÁSICO DE DRON

## ✔ activar control

```python id="control1"
client.enableApiControl(True)
client.armDisarm(True)
```

---

## ✔ despegar

```python id="takeoff"
client.takeoffAsync().join()
```

---

## ✔ mover el dron

```python id="move"
client.moveByVelocityAsync(0, 0, -2, 1).join()
```

* X → izquierda/derecha
* Y → adelante/atrás
* Z → arriba/abajo (negativo = subir)

---

## ✔ aterrizar

```python id="land"
client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)
```

---

# 🎮 CONTROL EN TIEMPO REAL (TU CASO)

La API permite comandos no bloqueantes:

```python id="async"
client.moveByVelocityAsync(1, 0, 0, 1)
```

👉 se ejecuta en background

---

# ⌨️ SCRIPT COMPLETO (BASE LIMPIA)

```python id="full"
import airsim
import time

client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)

client.takeoffAsync().join()

# mover adelante durante 2 segundos
client.moveByVelocityAsync(2, 0, 0, 2).join()

client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)
```

---

# 🧠 TIPOS DE CONTROL

## 1. Velocity control (el que usaste)

* rápido
* sencillo
* sin física compleja

---

## 2. Position control

```python id="pos"
client.moveToPositionAsync(10, 0, -5, 2).join()
```

---

## 3. Orientation control (yaw/pitch/roll)

```python id="orient"
client.rotateToYawAsync(90).join()
```

---

# ⚠️ ERRORES COMUNES (EN TU CASO)

## ❌ Python demasiado nuevo

* AirSim NO soporta bien Python 3.12+

## ❌ falta numpy

* rompe instalación inicial

## ❌ simulador no activo

* client.connect falla silenciosamente

---

# 🧭 RESUMEN CLARO

* Python API = cliente remoto
* no compila nada
* solo manda comandos al simulador
* depende de venv limpio + numpy + msgpack

---

# 🚀 IDEA FINAL

Si lo reduces a una frase:

> Python en AirSim solo es un “mando a distancia del dron”

