# 🚁 Guía: cambiar o crear una cámara “delantera” en FlightGear (FG)

Esta guía resume lo que estás haciendo (control por Web + bridge) y cómo **crear una cámara tipo helicóptero / frontal (nose cam)** o cambiar entre vistas correctamente.

---

# 🧠 1. Concepto clave (IMPORTANTE)

En FlightGear hay dos formas de “cámara”:

## 1) 📷 Vistas del sistema (views)
- cockpit
- chase
- tower
- custom views (1, 2, 3...)

👉 se cambian con:
```

/sim/current-view/view-number

```

---

## 2) 🎥 Offsets de cámara (lo que tú estás usando)

Esto:

```

/sim/current-view/heading-offset-deg
/sim/current-view/pitch-offset-deg

````

👉 NO crea una cámara nueva  
👉 solo mueve la orientación de la vista actual

---

# 🚁 2. Problema típico que tú tienes

Quieres:

> “una cámara delante del avión tipo helicóptero”

Pero estás usando:

- view actual + offsets

👉 eso SOLO funciona bien si la base view lo permite

---

# 🚀 3. SOLUCIÓN REAL: crear “cámara frontal”

Tienes 2 opciones:

---

# ✔ OPCIÓN A (rápida): usar view 1 + offsets

## 🔧 fuerza view estable

En FlightGear consola:

```nasal
setprop("/sim/current-view/view-number", 1);
````

o en telnet:

```
set /sim/current-view/view-number 1
```

---

## ✔ luego usas offsets

```
heading-offset-deg
pitch-offset-deg
```

👉 esto simula cámara frontal básica

---

# ✔ OPCIÓN B (PRO): crear cámara custom nasal

Esto es lo más parecido a “poner cámara delante del avión”

---

## 📁 archivo nasal

Crea:

```
$FG_ROOT/Nasal/frontcam.nas
```

---

## 🧠 código básico

```nasal
var frontCamInit = func {
    print("Front camera initialized");

    setprop("/sim/current-view/name", "frontcam");

    setprop("/sim/current-view/field-of-view", 60);

    # posición relativa al avión
    setprop("/sim/current-view/x-offset-m", 2.0);
    setprop("/sim/current-view/y-offset-m", 0.0);
    setprop("/sim/current-view/z-offset-m", -1.0);
}
```

---

## 🔧 activarlo en `autostart.nas`

```nasal
frontCamInit();
```

---

# 🚁 4. Cómo hacer cámara tipo helicóptero

Esto es lo que buscas realmente:

## 🎯 comportamiento:

* sigue avión
* está delante o ligeramente arriba
* no rota completamente con heading

---

## 🔧 valores típicos:

```
x-offset-m = +2 a +5   (delante)
y-offset-m = 0
z-offset-m = -1 a -2   (altura)
```

---

# 🧠 5. Diferencia importante

| Tipo          | Qué hace              |
| ------------- | --------------------- |
| offsets       | rota cámara           |
| custom camera | posiciona cámara real |
| view system   | cambia modo completo  |

---

# 🚀 6. Cómo integrarlo con TU sistema (Web + bridge)

Tu sistema actual:

```
HTML → WS → bridge → setprop offsets
```

👉 esto sigue siendo válido

---

## ✔ lo correcto sería:

### cámara base:

```
/sim/current-view/view-number = 1
```

### control:

```
heading-offset-deg
pitch-offset-deg
```

---

# ⚠️ 7. Problema típico que explicas tú

> “si el current view está en 15 no va pero en 1 sí”

✔ correcto

👉 porque view 15:

* puede bloquear offsets
* o usar lógica propia de cockpit

---

# 🚁 8. RECOMENDACIÓN FINAL (LA BUENA)

Para tu sistema Web:

## ✔ usa SIEMPRE:

```
view-number = 1
```

## ✔ controla con:

```
heading-offset-deg
pitch-offset-deg
```

## ❌ evita:

* cockpit view
* view 15 custom
* views que resetean cámara

---

# 🎮 9. Resultado esperado

Con esto tienes:

* cámara frontal estable ✔
* control Web funcionando ✔
* sin overrides raros ✔
* comportamiento tipo drone/helicóptero ✔

---

# 🚀 10. Si quieres siguiente nivel

Puedo darte:

### 🎥 cámara 100% independiente (sin view system)

### 🚁 helicóptero real con física de cámara

### 🎮 control tipo FPS mouse-lock

### 🧠 estabilización tipo gimbal (como GoPro)


