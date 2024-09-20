# ShadowID Developer Guide

## 🔧 **What’s Inside?**

Welcome to the developer's guide for **ShadowID**. This document will walk you through the inner workings of ShadowID, explaining the **code structure**, **core functionality**, and how the **authentication system** operates behind the scenes. Whether you’re contributing to the project or just curious about how everything fits together, this guide is here to help.

---

## 🗂 **Code Structure**

Here's a breakdown of the key directories and files in the project:

```bash
app/
├── auth.py             # Handles token generation (JWT) and OAuth2
├── config.py           # Configurations for settings (secret keys, expiration times, etc.)
├── db/
│   └── models.py       # Defines the database models (User model, etc.)
├── loggers.py          # Logger configuration for error tracking and debugging
├── routers/
│   ├── auth.py         # Routes for authentication (login, refresh tokens, register)
│   ├── user.py         # Routes for user-related endpoints (get current user, admin check)
├── security.py         # Handles encryption, token rotation, and rate-limiting
├── __init__.py         # App initialization
└── main.py             # Main entry point for FastAPI application
```

---

## 🛠 **Core Functionality**

### 1. **Authentication (OAuth2 and JWT)**

The main authentication flow of ShadowID relies on **OAuth2** for issuing tokens and **JWT** (JSON Web Tokens) for access control.

- **File**: `app/auth.py`
- **Key Functions**:
  - `create_access_token`: Generates a short-lived JWT access token that includes the user’s anonymous identifier.
  - `create_refresh_token`: Generates a longer-lived refresh token to renew the access token without requiring a new login.

#### How It Works

- **Login**: A user logs in by providing their anonymous identifier. If valid, ShadowID issues both an access token (short-lived) and a refresh token (long-lived).
- **Access Tokens**: The access token is included in the `Authorization` header for each request to protected routes. It’s validated by checking the token’s signature and expiration.
- **Refresh Tokens**: When the access token expires, the client can send the refresh token to the `/token/refresh` endpoint to get a new access token without having to log in again.

---

### 2. **Token Rotation and Storage**

One of the key features in ShadowID is **token rotation** for security. Each time a refresh token is used, a new refresh token is issued, and the old one is invalidated.

- **File**: `app/routers/auth.py` and `app/security.py`
- **Key Functions**:
  - `encrypt_data`: Encrypts refresh tokens before storing them in Redis, ensuring that sensitive tokens are protected.
  - `rotate_refresh_token`: Ensures that old tokens are deleted and replaced by new ones when they’re used to refresh an access token.

#### How token-rotation Works

- When a refresh token is presented, ShadowID encrypts the new refresh token before storing it in Redis.
- Old tokens are automatically invalidated by deleting them from Redis upon refresh.
- This adds an extra layer of security by ensuring that if a token is compromised, it won’t be usable for long.

---

### 3. **Rate-Limiting and Brute-Force Protection**

Rate-limiting prevents malicious actors from spamming the login endpoint to guess credentials.

- **File**: `app/security.py`
- **Key Functions**:
  - `is_rate_limited`: Checks if the user has exceeded the maximum allowed number of login attempts. If they have, further attempts are blocked for a specified duration.
  - `block_user`: Increments login attempts and blocks the user for a specified period if too many failed attempts are made.

#### How rate-limiting Works

- When a login attempt fails, ShadowID records this in Redis and increments the counter for the user’s identifier.
- After a certain number of failed attempts (configurable), further attempts are blocked for a certain time (e.g., 5 minutes).
- Redis is used to track login attempts and block duration, ensuring scalability and performance.

---

### 4. **Anonymous Identifiers**

ShadowID creates **anonymous identifiers** for users rather than using personal information like email addresses or phone numbers. This keeps the authentication process private.

- **File**: `app/routers/auth.py`
- **Key Function**:
  - `register_user`: Generates an anonymous identifier based on a user-supplied seed (e.g., a random string or device detail). This is stored securely in the database and used as the primary identifier for the user.

#### How anonymous-identifier Works

- When a user registers, they provide a **seed** (could be a random string, device info, etc.). This seed is processed to generate an anonymous identifier using a hashing algorithm (e.g., Argon2).
- The identifier is then stored in the **User** model, which is used for all future authentication without any personal information.

---

### 5. **Role-Based Access Control (RBAC)**

ShadowID supports **Role-Based Access Control** to restrict certain routes based on user roles (e.g., admin, user).

- **File**: `app/routers/user.py`
- **Key Function**:
  - `admin_endpoint`: Checks whether the logged-in user has the `admin` role before allowing access to admin-specific routes.

#### How RBAC Works

- Roles are defined in the `User` model, and the role is checked against the user's token when accessing protected routes.
- If the role doesn’t match (e.g., a regular user trying to access an admin route), the system returns a **403 Forbidden** response.

---

### 6. **Error Handling and Logging**

All errors are logged using a centralized logging system, making it easy to debug and monitor the app.

- **File**: `app/loggers.py`
- **Key Logging**: Each time an exception is raised (e.g., invalid credentials, expired token), it’s logged using `logger.error`. This makes debugging easy and provides visibility into what's happening under the hood.

---

## 🔧 **Configuration and Settings**

- **File**: `app/config.py`
- ShadowID uses environment-based configurations to keep things secure and flexible. Sensitive values like **secret keys** and **token expiration times** are stored here.
  
Make sure to set up your `.env` file with values for:

- `SECRET_KEY`: The key used to sign JWT tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The duration for which access tokens remain valid.
- `REFRESH_TOKEN_EXPIRE_MINUTES`: The expiration time for refresh tokens.
- Database connection strings and Redis configuration.

---

## 🔄 **Future Development**

Here are the key features we’re working on for ShadowID:

- **Zero-Knowledge Proofs (ZKP)**: We’re working on implementing ZKP authentication, which will allow users to prove their identity without revealing sensitive information. This is a cutting-edge privacy feature.
- **Multi-Factor Authentication (MFA)**: Adding a second layer of authentication for enhanced security.
- **Context-Aware RBAC**: Roles that adapt based on the context (time, location, etc.), providing more dynamic access control.
- **Federated Learning for Security**: Using federated learning to detect suspicious activity across users while preserving privacy.

---

## 💡 **Contributing to ShadowID**

Want to contribute? Here's how you can help:

1. **Fix a bug**: If you spot an issue, submit a fix!
2. **Add a feature**: Check our roadmap or addon new feature you’d like to work on.
3. **Improve documentation**: Got some ideas to improve this guide? Feel free to submit a PR.

Before you start, take a look at our `CONTRIBUTING.md` for guidelines.

---

## 🧑‍💻 **Final Words**

ShadowID is designed to be a privacy-first, cutting-edge authentication system, and we’re excited to see how you’ll use or contribute to it. Have any questions? Feel free to open an issue or reach out.

---

### **Let’s keep authentication secure, private, and anonymous!**

---

This **developer guide** provides a technical overview of how ShadowID operates. You can now maintain two README files:

- **README.md**: For end-users, providing a high-level overview of the project.
- **DEVELOPER_GUIDE.md**: For developers, providing detailed insight into the project’s functionality and structure.

Let me know if you'd like to tweak or add more specific details!
