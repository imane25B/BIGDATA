# 🚀 TP Big Data – Pipeline de Traitement Temps Réel

## 👩‍💻 Réalisé par :  
**BACHIRI Imane**

---

## 📌 Contexte

Dans un monde où les **données massives** sont omniprésentes, leur traitement en **temps réel** est devenu indispensable. Ce TP met en œuvre un pipeline de données utilisant les outils majeurs du Big Data :

- **Apache Kafka** pour la gestion des flux de données.
- **Apache Spark** pour le traitement en temps réel.
- **Docker** pour l'orchestration de l'environnement.
- **MinIO** pour le stockage objet (format Parquet).

---

## 🎯 Objectifs pédagogiques

- 📦 Déployer un environnement Big Data conteneurisé.
- 🔄 Gérer un flux de données via Kafka.
- ⚙️ Traiter et enrichir les données avec Spark Streaming.
- 🪣 Stocker les résultats dans MinIO au format **Parquet**.

---

## 📚 Compétences développées

✅ Déploiement d’un écosystème Big Data via Docker  
✅ Configuration de Kafka pour le streaming  
✅ Intégration de Spark Streaming avec Kafka  
✅ Application de transformations sur flux de données  
✅ Écriture/lecture de fichiers Parquet via MinIO

---

## 🔧 Pré-requis techniques

- Docker Desktop installé
- Python 3
- Java 8+
- Apache Spark
- Kafka (via Docker)
- MinIO (via Docker)

---

## 🏗️ Architecture du projet

```

+-------------+      Kafka      +-------------------+      Parquet      +---------+
\| capteur.py  |  ─────────────▶ | consumer\_spark.py |  ───────────────▶ | MinIO   |
\| (Producer)  |                |   (Spark Streaming)|                  | Storage |
+-------------+                +-------------------+                  +---------+

````

---

## ⚙️ Composants testés

| Composant | Vérification |
|----------|--------------|
| Docker   | ✅ `docker ps` |
| Java     | ✅ `java -version` |
| Spark    | ✅ `spark-submit --version` |

---

## 🚀 Mise en œuvre

### 1️⃣ Démarrage des services Docker

```bash
docker-compose up -d
````

Vérifier que les services Kafka, Zookeeper, MinIO, Spark sont bien lancés.

---

### 2️⃣ Producteur Kafka (Python)

Fichier : `capteur.py`

* Génère des données simulées.
* Envoie les messages JSON dans un **topic Kafka**.

Exemple de message envoyé :

```json
{"transaction_id": 123, "montant": 100, "devise": "USD", "timestamp": "..."}
```

---

### 3️⃣ Traitement Spark Streaming

Fichier : `consumer_spark.py`

* Lit les messages depuis Kafka.
* Convertit les devises (USD → EUR).
* Transforme la date, ajoute le fuseau horaire.
* Filtre les erreurs / données incomplètes.
* Enregistre les résultats dans **MinIO** (`/output/`) en **Parquet**.

---

### 4️⃣ Accès aux résultats sur MinIO

* URL : [http://localhost:9001](http://localhost:9001)
* **Username** : `Minio`
* **Password** : `Minio123`

Vérifie les buckets :

* `/transactions/output/` → fichiers Parquet
* `/transactions/checkpoint/` → état Spark

---

## 🧪 Exécution des scripts

1. Lancer les containers :

```bash
docker-compose up -d
```

2. Lancer Spark (consumer) :

```bash
spark-submit consumer_spark.py
```

3. Lancer le producteur (Python) :

```bash
python capteur.py
```

---

## ✅ Résultat attendu

* Kafka reçoit les messages produits par `capteur.py`
* Spark traite les messages et écrit les données enrichies dans MinIO
* Les fichiers `.parquet` sont accessibles et lisibles par Spark ou tout autre moteur Big Data

---

## 💡 Améliorations possibles

* Ajout de monitoring avec Grafana + Prometheus
* Stockage vers un Data Lake (HDFS ou S3 simulé)
* Ajout d’un module de machine learning pour scoring des transactions

---

## 📜 Licence

Projet académique – Usage libre à des fins pédagogiques.
