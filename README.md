# ShadowID: Privacy-Focused Authentication System

## 🚀 Purpose

Welcome to **ShadowID**, where your privacy is a priority! In a world where your personal data is treated like gold (or sometimes like a piñata at a hacker’s party), ShadowID offers a solution that makes sure you can authenticate securely, **without revealing any personal identifiers**. ShadowID is designed to provide **anonymous, privacy-first authentication**, using cutting-edge techniques to keep your data yours.

Think of ShadowID as your secret identity on the web—whether you’re Batman or Wonder Woman, your personal data stays safe while still giving you the power to log in, authenticate, and manage sessions securely.

---

## 🔐 Features We Have So Far

### 1. **Anonymous Identifiers**

No need to provide personal information like email addresses or phone numbers to authenticate. We generate secure, **anonymous identifiers** for each user based on a seed (could be a device detail or a random string). This keeps things private and simple—like having a secret identity.

### 2. **OAuth2 with JWT (JSON Web Tokens)**

ShadowID uses **OAuth2** for authentication with **JWT** to issue access tokens. These tokens are lightweight and secure, ensuring that only the right people (or anonymous identifiers) can access the system.

### 3. **Refresh Tokens (with Hashing)**

We've taken security up a notch. **Refresh tokens** allow users to stay logged in without having to re-authenticate every few minutes. For safety these tokens are stored in Redis **after being hashed**, so even if Redis is compromised the raw tokens remain secret.

### 4. **Token Rotation**

Old refresh tokens? No problem. We **rotate tokens** on each refresh, making sure that your session is always fresh and secure. When a new token is issued, the old one is thrown out. Like changing the locks on your door after every guest leaves.

### 5. **Rate-Limiting for Brute-Force Protection**

Nobody likes a brute—especially brute-force attackers. We’ve implemented **rate-limiting** on login attempts, meaning that after a few failed tries, users have to wait a bit before trying again. This ensures that hackers can’t keep knocking at the door.

### 6. **Role-Based Access Control (RBAC)**

Not everyone is an admin. We’ve got **RBAC** in place to control who can access what. Whether you're a user or an admin, you’ll only have access to the features meant for you. No peeking behind the curtains!

---

## 🛠️ Features We’re Working On (Stay Tuned!)

### 1. **Zero-Knowledge Proof Authentication (ZKP)**

We’re diving deep into cryptography and working on **Zero-Knowledge Proofs** (ZKP), where you can prove you know a secret without actually revealing the secret itself. It’s like showing you have the keys to the vault, without anyone seeing the keys.

### 2. **Context-Aware Role-Based Access Control**

RBAC is great, but what if your permissions changed based on where or when you're logging in? We’re building **context-aware RBAC**, so certain actions can be allowed or restricted depending on factors like time of day or location. The system gets smarter, and security becomes even tighter.

### 3. **Federated Learning for Anomaly Detection**

In the near future, we’re planning to leverage **Federated Learning** for anomaly detection. This will allow us to detect suspicious behaviors in a privacy-friendly way, helping prevent unauthorized access before it even happens.

### 4. **Multi-Factor Authentication (MFA)**

More layers of security are coming your way! Soon, we’ll be integrating **Multi-Factor Authentication (MFA)**, allowing users to verify their identity with a second factor (like a code sent to their phone). It’s another line of defense to keep accounts secure.

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.8+**
- **PostgreSQL** (for database)
- **Redis** (for token and session management)

### Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/adarshmalviy/ShadowID.git
    cd ShadowID
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your `.env` file** with your configurations (database, secret keys, etc.).

5. **Start the FastAPI server**:

    ```bash
    fastapi run
    ```

6. Head to the interactive API docs at:

    ```bash
    http://127.0.0.1:8000/sldoc
    ```

---

## 🔧 Usage

### Register a New User

You can register a new user by posting a seed to the `/register` endpoint, and ShadowID will generate an anonymous identifier for you:

```json
{
  "seed": "random-string"
}
```

### Login with Anonymous Identifier

Once registered, you can log in using your anonymous identifier, and ShadowID will issue an **access token** and **refresh token**:

```json
{
  "anonymous_identifier": "your_anonymous_identifier"
}
```

### Refresh Tokens

To keep your session active, just send your **refresh token** to `/token/refresh`, and ShadowID will give you a fresh set of tokens.

---

## 🧑‍💻 Contributing

Want to help make ShadowID even better? We welcome contributions! Whether it’s fixing bugs, implementing new features, or adding tests, feel free to jump in.

Here’s how to get started:

1. **Fork the repo**.
2. Create your own branch (`git checkout -b your-feature-branch`).
3. Make your changes.
4. **Submit a pull request** with a clear description of the changes you’ve made.

Let’s build something great together!

---

## 👨‍💻 Maintainers

- **Adarsh Malviya** (<adarshmalvi77@gmail.com>)
- Other contributors are always welcome!

---

## License

This project is licensed under the **MIT License**—enjoy responsibly!

---

### 🚀 Stay tuned for more updates as we continue to make ShadowID more secure, more private, and more fun to use

---

Let me know if there are any specific areas you'd like to adjust or expand on!
