# Modélisation de la Probabilité de Défaut (PD) – Projet Scoring Crédit

## Description du projet

Ce projet a pour objectif de construire un **modèle de scoring estimant la probabilité de défaut (PD)** à un an d'une clientèle de particuliers, dans le cadre de la modélisation du risque de crédit (approche IRB).

La démarche suit les étapes d'un projet de modélisation bancaire :

1. **Exploration et préparation des données** : description des variables, traitement des valeurs manquantes et contrôle de qualité.
2. **Segmentation du portefeuille** en trois populations homogènes en termes de risque : *BPGF* (Banque Privée / Gestion de Fortune), *Non-BPGF mono-tiers* et *Non-BPGF multi-tiers*.
3. **Analyse de la variable cible** (`ddefaut_ndb`) et des taux de défaut par segment.
4. **Sélection et discrétisation des variables explicatives**, puis construction du modèle de score.
5. **Calibrage de la PD** et constitution des classes homogènes de risque.
6. **Validation du modèle** : pouvoir discriminant, stabilité et qualité du calibrage.

## Structure du dépôt



## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Auteurs

- KENNE YONTA Lesline
- OUATTARA Irma
- AHUI Yann

*Projet réalisé dans le cadre du cours de Scoring – 2026.*

