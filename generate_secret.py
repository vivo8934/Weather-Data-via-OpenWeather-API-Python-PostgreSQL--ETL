#!/usr/bin/env python3
import os
import secrets

def get_or_generate_secret_key(env_var="AIRFLOW__WEBSERVER__SECRET_KEY", length=32):
    # Try to read from env
    key = os.getenv(env_var)
    if key:
        print(f"{env_var} is already set:")
        print(key)
        return key

    # Generate a new URL-safe token
    new_key = secrets.token_urlsafe(length)
    print(f"{env_var} was not set. Generated new key:")
    print(new_key)
    return new_key

if __name__ == "__main__":
    get_or_generate_secret_key()
