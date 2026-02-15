#!/usr/bin/env python3
"""
Sandinas Plugin Installer (Windows)

Configura el plugin para Windows.
Crea un archivo .installed cuando termina exitosamente para no volver a ejecutarse.
"""

import sys
from pathlib import Path


def is_already_installed(plugin_root: Path) -> bool:
    """Verifica si el plugin ya esta instalado"""
    installed_flag = plugin_root / ".installed"
    return installed_flag.exists()


def mark_installed(plugin_root: Path):
    """Marca el plugin como instalado"""
    installed_flag = plugin_root / ".installed"
    installed_flag.touch()


def install_hooks(plugin_root: Path, verbose: bool = True):
    """Instala los hooks para Windows"""
    hooks_dir = plugin_root / "hooks"

    if not hooks_dir.exists():
        if verbose:
            print(f"ERROR: Directorio hooks no encontrado en {hooks_dir}")
        return False

    if verbose:
        print(f"Plataforma: Windows")
        print(f"Hooks configurados: {hooks_dir / 'hooks.json'}")

    # Marcar como instalado
    mark_installed(plugin_root)
    return True


def main():
    # Obtener el directorio del plugin (donde esta este script)
    script_path = Path(__file__).resolve()
    plugin_root = script_path.parent

    # Verificar si ya esta instalado
    if is_already_installed(plugin_root):
        # Ya instalado, salir silenciosamente (para auto-install desde SessionStart)
        return 0

    # Modo verbose: mostrar mensajes
    print(f"Configurando plugin: {plugin_root.name}")
    print("-" * 50)

    if install_hooks(plugin_root, verbose=True):
        print("-" * 50)
        print("OK: Plugin configurado correctamente")
        return 0
    else:
        print("-" * 50)
        print("ERROR: Fallo al configurar plugin")
        return 1


if __name__ == "__main__":
    sys.exit(main())
