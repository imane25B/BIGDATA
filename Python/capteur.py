from kafka import KafkaProducer
import datetime as dt
from datetime import timezone
import json
import random
import time
import uuid

def generate_transaction():
    transaction_types = ['achat', 'remboursement', 'transfert']
    payment_methods = ['carte_de_credit', 'especes', 'virement_bancaire', 'erreur']
    Villes = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", None]
    Rues = ["Rue de la République", "Rue de Paris", "Rue Auguste Delaune", None]
    
    current_time = dt.datetime.now(timezone.utc).isoformat()
    
    transaction_data = {
        "id_transaction": str(uuid.uuid4()),
        "type_transaction": random.choice(transaction_types),
        "montant": round(random.uniform(10.0, 1000.0), 2),
        "devise": random.choice(["EUR", "USD"]),
        "date": current_time,
        "lieu": f"{random.choice(Rues)}, {random.choice(Villes)}",
        "moyen_paiement": random.choice(payment_methods),
        "produit": f"Produit{random.randint(1, 100)}",
        "quantite": random.randint(1, 10),
        "prix_unitaire": round(random.uniform(5.0, 200.0), 2),
        "id_utilisateur": f"User{random.randint(1, 1000)}",
        "nom_utilisateur": f"Utilisateur{random.randint(1, 1000)}",
        "adresse_utilisateur": f"{random.randint(1, 1000)} {random.choice(Rues)}, {random.choice(Villes)}",
        "email_utilisateur": f"utilisateur{random.randint(1, 1000)}@example.com"
    }
    
    # Conversion USD en EUR
    if transaction_data["devise"] == "USD":
        transaction_data["montant"] = round(transaction_data["montant"] * 0.85, 2)
        transaction_data["devise"] = "EUR"
    
    # Vérifier et supprimer les transactions en erreur ou avec des valeurs None
    if transaction_data["moyen_paiement"] == "erreur" or \
       None in [transaction_data["lieu"], transaction_data["adresse_utilisateur"]]:
        return None
        
    return transaction_data

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=json_serializer
)

def produce_transactions(num_transactions=100):
    try:
        for _ in range(num_transactions):
            transaction = generate_transaction()
            if transaction:
                producer.send('transactions', transaction)
                print(f"Sent transaction: {transaction['id_transaction']}")
            time.sleep(1)
    except Exception as e:
        print(f"Error producing messages: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    produce_transactions()
