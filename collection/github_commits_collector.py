"""
GitHub Commits Collector
=========================

Recolecta commits relacionados con un issue específico desde la API de GitHub.
"""

import requests
import time

OWNER = "jabref"
REPO = "jabref"

# Rate limiting: GitHub permite 60 peticiones/hora sin autenticación
# Con autenticación: 5000 peticiones/hora
# Agregamos un pequeño delay para evitar problemas
DELAY_BETWEEN_REQUESTS = 0.1  # segundos


def collect_commits(issue_number):
    """
    Recolecta mensajes de commits relacionados con un issue.
    
    Args:
        issue_number: Número del issue en GitHub
        
    Returns:
        list: Lista de mensajes de commits relacionados
    """
    try:
        # Obtener eventos del issue
        events_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/events"
        
        response = requests.get(events_url, timeout=10)
        
        if response.status_code != 200:
            # Si el issue no existe o hay error, retornar lista vacía
            if response.status_code == 404:
                return []
            # Para otros errores, imprimir pero continuar
            if response.status_code == 403:
                # Rate limit alcanzado
                print(f"        ⚠ Rate limit alcanzado para issue #{issue_number}")
                time.sleep(60)  # Esperar 1 minuto
                return []
            return []
        
        events = response.json()
        
        if not isinstance(events, list):
            return []
        
        commit_messages = []
        referenced_commits = 0
        
        # Buscar eventos de tipo "referenced" que mencionen commits
        for event in events:
            if event.get("event") == "referenced" and "commit_id" in event:
                referenced_commits += 1
                commit_id = event["commit_id"]
                commit_url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{commit_id}"
                
                try:
                    commit_response = requests.get(commit_url, timeout=10)
                    
                    if commit_response.status_code == 200:
                        commit_data = commit_response.json()
                        commit_message = commit_data.get("commit", {}).get("message", "")
                        if commit_message:
                            commit_messages.append(commit_message)
                    
                    # Pequeño delay para evitar rate limiting
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    
                except Exception as e:
                    # Si falla obtener un commit específico, continuar con el siguiente
                    continue
        
        return commit_messages
        
    except requests.exceptions.Timeout:
        print(f"        ⚠ Timeout al obtener commits para issue #{issue_number}")
        return []
    except requests.exceptions.ConnectionError:
        print(f"        ⚠ Error de conexión al obtener commits para issue #{issue_number}")
        return []
    except Exception as e:
        # Cualquier otro error, retornar lista vacía pero no fallar
        return []
