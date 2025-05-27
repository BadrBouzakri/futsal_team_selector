# Politique de Sécurité

## Versions Supportées

Les versions suivantes du Générateur d'Équipes Futsal sont actuellement supportées avec des mises à jour de sécurité :

| Version | Supportée          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Signaler une Vulnérabilité

Si vous découvrez une vulnérabilité de sécurité, veuillez **NE PAS** créer d'issue publique.

Au lieu de cela, veuillez :

1. Envoyer un email à l'équipe de sécurité
2. Inclure une description détaillée de la vulnérabilité
3. Fournir des étapes pour reproduire le problème
4. Indiquer l'impact potentiel

## Processus de Réponse

1. **Accusé de réception** : Nous accuserons réception de votre rapport dans les 48 heures
2. **Évaluation** : Nous évaluerons la vulnérabilité et déterminerons sa sévérité
3. **Correction** : Nous développerons et testerons un correctif
4. **Publication** : Nous publierons le correctif et créditerons le rapporteur

## Mesures de Sécurité Implémentées

### Application Web
- ✅ Sessions sécurisées avec cookies HTTPOnly
- ✅ Protection CSRF implicite via Flask
- ✅ Validation des données d'entrée
- ✅ Authentification pour l'administration
- ✅ Pas de stockage de données sensibles

### Infrastructure Docker
- ✅ Conteneur non-root pour l'exécution
- ✅ Image de base minimale (Python slim)
- ✅ Variables d'environnement pour la configuration
- ✅ Healthcheck pour la surveillance
- ✅ Volumes pour la persistance des données

### Configuration
- ✅ Variables d'environnement pour les secrets
- ✅ Configuration séparée pour dev/prod
- ✅ Logs rotatifs pour éviter la saturation
- ✅ Pas de secrets hardcodés dans le code

## Recommandations de Déploiement

### Production
1. **Variables d'environnement** :
   ```bash
   SECRET_KEY=your-strong-random-secret-key
   ADMIN_PASSWORD=strong-admin-password
   SESSION_COOKIE_SECURE=true
   ```

2. **Proxy inverse** :
   - Utilisez Nginx ou Apache comme proxy
   - Configurez HTTPS/SSL
   - Limitez le taux de requêtes

3. **Firewall** :
   - Exposez seulement le port nécessaire
   - Limitez l'accès administrateur
   - Surveillez les tentatives de connexion

4. **Mises à jour** :
   - Maintenez les dépendances à jour
   - Surveillez les alertes de sécurité
   - Testez les mises à jour en environnement de test

### Monitoring
- Surveillez les logs d'accès
- Alertes sur les tentatives de connexion échouées
- Monitoring des ressources système
- Sauvegarde régulière des données

## Conformité et Bonnes Pratiques

### RGPD / Protection des Données
- Aucune donnée personnelle collectée par défaut
- Historique local non lié à des utilisateurs
- Possibilité d'effacer l'historique
- Pas de tracking ou analytics

### Sécurité du Code
- Code ouvert pour audit public
- Dépendances minimales et sécurisées
- Pas d'exécution de code utilisateur
- Validation stricte des entrées

## Audit de Sécurité

Pour effectuer un audit de sécurité de base :

```bash
# Vérifier les dépendances vulnérables
pip audit

# Scanner l'image Docker
docker scout cves futsal-teams-app

# Vérifier la configuration
./start.sh status
```

## Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask-security-too.readthedocs.io/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Python Security](https://python-security.readthedocs.io/)

---

**La sécurité est une responsabilité partagée. Merci de nous aider à maintenir cette application sécurisée !** 🔒