#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVP Test script para zhipu AI usando OpenAI SDK
Verifica API key y prueba modelos disponibles
"""
import os
import sys

# Fix encoding for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package no instalado")
    print("Ejecutar: pip install openai")
    sys.exit(1)

def test_with_openai_sdk():
    """Test using OpenAI SDK compatible with zhipu AI."""
    api_key = os.environ.get("ZHIPUAI_API_KEY")
    if not api_key:
        print("ERROR: ZHIPUAI_API_KEY no configurada")
        return

    print(f"API Key: {api_key[:20]}...")
    print("\nUsando OpenAI SDK con zhipu AI")
    print("=" * 50)

    # zhipu AI usa OpenAI-compatible API
    client = OpenAI(
        api_key=api_key,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )

    # Modelos a probar (documentacion oficial 2025)
    models = [
        "glm-4-flash",
        "glm-4-flashx",
        "glm-4.7",
        "glm-4.6",
        "glm-4.5",
        "glm-4-air",
        "glm-4-plus",
    ]

    working = []
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hola"}],
                max_tokens=10,
                timeout=5
            )
            content = response.choices[0].message.content
            print(f"[OK] {model}: {content[:30]}")
            working.append(model)
            break  # Primer modelo que funciona es suficiente
        except Exception as e:
            err = str(e)
            if "429" in err or "1113" in err:
                print(f"[SALDO] {model}: Modelo existe pero saldo insuficiente")
                working.append(model)  # Existe, solo falta saldo
                break
            elif "1211" in err or "400" in err:
                print(f"[NO] {model}: No existe")
            else:
                print(f"[ERR] {model}: {err[:40]}")

    # Test de clasificacion simple
    if working:
        print(f"\nModelo disponible: {working[0]}")
        print("\nTest de clasificacion:")
        print("-" * 30)

        prompt = "arreglar el bug del login"
        system = """Responde SOLO con JSON:
{
    "clear_context": true/false,
    "reasoning": "explicacion"
}"""

        try:
            response = client.chat.completions.create(
                model=working[0],
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=150
            )
            result = response.choices[0].message.content
            print(f"Prompt: {prompt}")
            print(f"LLM Response: {result}")
        except Exception as e:
            print(f"Error en test: {e}")

if __name__ == "__main__":
    test_with_openai_sdk()
