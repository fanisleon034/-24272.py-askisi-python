import json
import matplotlib.pyplot as plt
from collections import Counter

def load_quotes():
    """
    Φορτώνει τα δεδομένα από το αρχείο quotes.json.
    """
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)
    return quotes

def plot_histogram(quotes):
    """
    Δημιουργεί και αποθηκεύει ένα ιστογράφημα που δείχνει τον αριθμό των αποφθεγμάτων ανά συγγραφέα.
    Στον άξονα x εμφανίζονται τα ονόματα των συγγραφέων (ταξινομημένα κατά αριθμό αποφθεγμάτων από το μεγαλύτερο στο μικρότερο),
    και στον άξονα y ο αριθμός των αποφθεγμάτων.
    Το γράφημα αποθηκεύεται ως 'histogram.png'.
    """
    # Εξαγωγή ονομάτων συγγραφέων από τα δεδομένα
    authors = [quote["author"] for quote in quotes]
    # Μέτρηση των εμφανίσεων κάθε συγγραφέα
    counts = Counter(authors)
    # Ταξινόμηση συγγραφέων με βάση τον αριθμό των αποφθεγμάτων σε φθίνουσα σειρά
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    author_names = [x[0] for x in sorted_counts]
    num_quotes = [x[1] for x in sorted_counts]

    plt.figure(figsize=(10, 6))
    plt.bar(author_names, num_quotes, color='skyblue')
    plt.xlabel("Συγγραφείς")
    plt.ylabel("Αριθμός αποφθεγμάτων")
    plt.title("Αριθμός αποφθεγμάτων ανά συγγραφέα")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("histogram.png")
    plt.show()
    print("Το ιστογράφημα αποθηκεύτηκε ως 'histogram.png'.")

def main():
    quotes = load_quotes()
    plot_histogram(quotes)

if __name__ == "__main__":
    main()
