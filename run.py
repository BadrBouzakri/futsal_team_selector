#!/usr/bin/env python
"""
Script de démarrage pour l'application Futsal Team Selector en mode développement
Usage: python run.py [--debug] [--host=0.0.0.0] [--port=5000]
"""

import os
import sys
import argparse

from app import create_app

def parse_arguments():
    """Parse les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(description='Démarrer le serveur Futsal Team Selector')
    
    parser.add_argument('--debug', action='store_true', help='Activer le mode debug')
    parser.add_argument('--host', default='0.0.0.0', help='Hôte sur lequel écouter (défaut: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port sur lequel écouter (défaut: 5000)')
    parser.add_argument('--env', default='development', choices=['development', 'testing', 'production'],
                       help='Environnement à utiliser (défaut: development)')
    
    return parser.parse_args()

def main():
    """Fonction principale pour démarrer l'application"""
    args = parse_arguments()
    
    # Définir les variables d'environnement
    os.environ['FLASK_ENV'] = args.env
    if args.debug:
        os.environ['FLASK_DEBUG'] = '1'
    
    # Créer l'application avec la configuration appropriée
    app = create_app(args.env)
    
    # Configurer les options de démarrage
    run_options = {
        'host': args.host,
        'port': args.port,
        'debug': args.debug,
        'use_reloader': args.debug,
        'threaded': True
    }
    
    # Affichage des informations de démarrage
    print(f"Démarrage du serveur Futsal Team Selector en mode {args.env}")
    print(f"URL d'accès: http://{args.host}:{args.port}")
    print("Appuyez sur CTRL+C pour arrêter le serveur")
    
    # Démarrer l'application
    app.run(**run_options)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
