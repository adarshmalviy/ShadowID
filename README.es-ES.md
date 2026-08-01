

# ShadowID: Sistema de Autenticación Centrada en la Privacidad

## 🚀 Propósito

¡Bienvenido a **ShadowID**, donde tu privacidad es una prioridad! En un mundo donde tus datos personales se tratan como oro (o a veces como una piñata en una fiesta de hackers), ShadowID ofrece una solución que garantiza que puedas autenticarte de forma segura, **sin revelar ningún identificador personal**. ShadowID está diseñado para proporcionar **autenticación anónima y priorizada en la privacidad**, utilizando técnicas de vanguardia para mantener tus datos bajo tu control.

Piensa en ShadowID como tu identidad secreta en la web: seas Batman o Wonder Woman, tus datos personales permanecerán a salvo mientras te ofrecemos el poder de iniciar sesión, autenticarte y gestionar sesiones de forma segura.

---

## 🔐 Funciones Disponibles

### 1. **Identificadores Anónimos**

No es necesario proporcionar información personal como direcciones de correo electrónico o números de teléfono para autenticarte. Generamos **identificadores anónimos** seguros para cada usuario basados en una semilla (seed) (puede ser un detalle del dispositivo o una cadena aleatoria). Esto mantiene las cosas privadas y simples, como tener una identidad secreta.

### 2. **OAuth2 con JWT (JSON Web Tokens)**

ShadowID utiliza **OAuth2** para la autenticación con **JWT** para emitir tokens de acceso. Estos tokens son ligeros y seguros, garantizando que solo las personas correctas (o identificadores anónimos) puedan acceder al sistema.

### 3. **Tokens de Renovación (con Hashing)**

Hemos elevado la seguridad un nivel. Los **tokens de renovación** permiten a los usuarios permanecer conectados sin tener que volver a autenticarse cada pocos minutos. Por seguridad, estos tokens se almacenan en Redis **después de ser hasheados**, por lo que incluso si Redis se ve comprometido, los tokens originales permanecen secretos.

### 4. **Rotación de Tokens**

¿Tokens de renovación antiguos? No hay problema. **Rotamos los tokens** en cada renovación, asegurando que tu sesión siempre sea fresca y segura. Cuando se emite un nuevo token, el anterior se descarta. Es como cambiar las cerraduras de tu puerta después de que cada invitado se vaya.

### 5. **Limitación de Tasa (Rate-Limiting) para Protección contra Fuerza Bruta**

A nadie le gusta un bruto, especialmente a los atacantes de fuerza bruta. Hemos implementado **limitación de tasa** en los intentos de inicio de sesión, lo que significa que después de unos pocos intentos fallidos, los usuarios deben esperar un tiempo antes de volver a intentarlo. Esto asegura que los hackers no puedan seguir llamando a la puerta.

### 6. **Control de Acceso Basado en Roles (RBAC)**

No todos son administradores. Tenemos **RBAC** implementado para controlar quién puede acceder a qué. Ya seas un usuario o un administrador, solo tendrás acceso a las funciones diseñadas para ti. ¡Sin mirar detrás de las cortinas!

---

## 🛠️ Funciones en Desarrollo (¡No dejes de seguirnos!)

### 1. **Autenticación con Prueba de Conocimiento Cero (ZKP)**

Estamos profundizando en la criptografía y trabajando en **Pruebas de Conocimiento Cero** (ZKP), donde puedes demostrar que conoces un secreto sin revelar el secreto en sí. Es como demostrar que tienes las llaves de la caja fuerte, sin que nadie vea las llaves.

### 2. **Control de Acceso Basado en Roles Consciente del Contexto**

El RBAC es genial, pero ¿qué pasaría si tus permisos cambiaran según desde dónde o cuándo inicias sesión? Estamos construyendo un **RBAC consciente del contexto**, para que ciertas acciones se permitan o restrinjan dependiendo de factores como la hora del día o la ubicación. El sistema se vuelve más inteligente y la seguridad se vuelve aún más estricta.

### 3. **Aprendizaje Federado para Detección de Anomalías**

En un futuro cercano, planeamos aprovechar el **Aprendizaje Federado** para la detección de anomalías. Esto nos permitirá detectar comportamientos sospechosos de una manera respetuosa con la privacidad, ayudando a prevenir el acceso no autorizado antes de que ocurra.

### 4. **Autenticación Multifactor (MFA)**

¡Llegan más capas de seguridad! Pronto integraremos la **Autenticación Multifactor (MFA)**, permitiendo a los usuarios verificar su identidad con un segundo factor (como un código enviado a su teléfono). Es otra línea de defensa para mantener las cuentas seguras.

---

## 🛠️ Comenzar

### Prerrequisitos

- **Python 3.8+**
- **PostgreSQL** (para la base de datos)
- **Redis** (para la gestión de tokens y sesiones)

### Instrucciones de Configuración

1. **Clona el repositorio**:

    ```bash
    git clone https://github.com/adarshmalviy/ShadowID.git
    cd ShadowID
    ```

2. **Crea un entorno virtual**:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Instala las dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configura tu `.env` file** con tus configuraciones (base de datos, claves secretas, etc.).

5. **Inicia el servidor FastAPI**:

    ```bash
    fastapi run
    ```

6. Dirígete a la documentación interactiva de la API en:

    ```bash
    http://127.0.0.1:8000/sldoc
    ```

---

## 🔧 Uso

### Registrar un Nuevo Usuario

Puedes registrar un nuevo usuario enviando una semilla al punto final `/register`, y ShadowID generará un identificador anónimo para ti:

```json
{
  "seed": "random-string"
}
```

### Iniciar Sesión con Identificador Anónimo

Una vez registrado, puedes iniciar sesión usando tu identificador anónimo, y ShadowID te emitirá un **token de acceso** y un **token de renovación**:

```json
{
  "anonymous_identifier": "your_anonymous_identifier"
}
```

### Renovar Tokens

Para mantener tu sesión activa, simplemente envía tu **token de renovación** a `/token/refresh`, y ShadowID te proporcionará un conjunto fresco de tokens.

---

## 🧑‍💻 Contribuir

¿Quieres ayudar a mejorar ShadowID? ¡Bienvenidas las contribuciones! Ya sea corrigiendo errores, implementando nuevas funciones o agregando pruebas, siéntete libre de sumarte.

Así es como puedes comenzar:

1. **Haz un fork del repositorio**.
2. Crea tu propia rama (`git checkout -b your-feature-branch`).
3. Realiza tus cambios.
4. **Envía un pull request** con una descripción clara de los cambios que has realizado.

¡Construyamos algo genial juntos!

---

## 👨‍💻 Mantenimiento

- **Adarsh Malviya** (<adarshmalvi77@gmail.com>)
- ¡Siempre son bienvenidos otros colaboradores!

---

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**: ¡disfrútalo responsablemente!

---

### 🚀 Mantente atento a más actualizaciones mientras continuamos haciendo que ShadowID sea más seguro, más privado y más divertido de usar

---

¡Avísame si hay alguna área específica que te gustaría ajustar o expandir!
