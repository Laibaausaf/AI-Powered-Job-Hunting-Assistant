# API Contract

## 1. Purpose

This document defines the communication contract between the frontend and backend.

The frontend communicates with the backend through HTTP REST APIs.

The frontend should not directly access the database.

The frontend should not directly call private AI APIs.

---

# 2. Base URL

During local development:

```text
http://127.0.0.1:8000