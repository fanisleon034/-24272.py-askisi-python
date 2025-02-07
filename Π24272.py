import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import quote  

def extract_quote_ids(am):
    url = f"https://tma111.netlify.app/.netlify/functions/generate?id={am}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Σφάλμα κατά το request στη σελίδα.")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    
    numbers = []
    
    tags = soup.find_all(['div', 'p', 'span', 'li', 'td'])
    for tag in tags:
      
        if tag.get('id') == 'colors':
            continue
       
        if tag.string:
            text = tag.string.strip()
            if text.isdigit():
                numbers.append(int(text))
            else:
                
                for part in text.split():
                    if part.isdigit():
                        numbers.append(int(part))
                    else:
                        digits = ''.join([c for c in part if c.isdigit()])
                        if digits != "":
                            numbers.append(int(digits))
        else:
           
            text = tag.get_text(" ", strip=True)
            for part in text.split():
                if part.isdigit():
                    numbers.append(int(part))
                else:
                    digits = ''.join([c for c in part if c.isdigit()])
                    if digits:
                        numbers.append(int(digits))
   
    unique_numbers = list(dict.fromkeys(numbers))
    return unique_numbers

def extract_colors(soup):
    colors_div = soup.find("div", id="colors")
    if not colors_div:
        return ("1866db", "fdfff31")
    style = colors_div.get("style", "")
    bg_color = None
    text_color = None
    for part in style.split(";"):
        part = part.strip()
        if part.startswith("background-color:"):
            bg_color = part.split("background-color:")[1].strip()
        elif part.startswith("color:"):
            text_color = part.split("color:")[1].strip()
    
    if bg_color and bg_color.startswith("#"):
        bg_color = bg_color[1:]
    if text_color and text_color.startswith("#"):
        text_color = text_color[1:]
    if not bg_color:
        bg_color = "1866db"
    if not text_color:
        text_color = "fdfff31"
    return (bg_color, text_color)

def retrieve_quote(quote_id):
    
    if not (1 <= quote_id <= 30):
        print(f"Παράβεται το επιτρεπόμενο εύρος για το quote id {quote_id}. Παράλειψη.")
        return None
    url = f"https://dummyjson.com/quotes/{quote_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Σφάλμα ανάκτησης για το quote id {quote_id}")
        return None
    data = response.json()
    if "id" in data and "quote" in data and "author" in data:
        return {"id": data["id"], "quote": data["quote"], "author": data["author"]}
    else:
        return None


def save_quotes(quotes_list):
    sorted_quotes = sorted(quotes_list, key=lambda x: x["id"])
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(sorted_quotes, f, ensure_ascii=False, indent=4)
    print("Το αρχείο quotes.json αποθηκεύτηκε επιτυχώς.")

def generate_quote_image(quote_item, bg_color, text_color):
    base_url = "https://dummyjson.com/image/1200x200"
   
    text_param = quote(quote_item["quote"])
    image_url = f"{base_url}/{bg_color}/{text_color}?text={text_param}&fontSize=18"
    response = requests.get(image_url)
    if response.status_code == 200:
        folder = "quotes"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, f"{quote_item['id']}.png")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Η εικόνα για το quote id {quote_item['id']} αποθηκεύτηκε: {filename}")
    else:
        print(f"Σφάλμα κατά τη δημιουργία εικόνας για το quote id {quote_item['id']}")

def main():
    am = "Π24272"
    print(f"Εκκίνηση με Α.Μ.: {am}")
    
  
    url = f"https://tma111.netlify.app/.netlify/functions/generate?id={am}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Σφάλμα κατά τη φόρτωση της δυναμικής σελίδας.")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    
   
    quote_ids = extract_quote_ids(am)
    print("Εξαγόμενα Quote IDs:")
    print(quote_ids)
    
    
    bg_color, text_color = extract_colors(soup)
    print(f"Χρησιμοποιούνται: background color #{bg_color} και text color #{text_color}")
    
 
    quotes = []
    for qid in quote_ids:
        quote_data = retrieve_quote(qid)
        if quote_data:
            quotes.append(quote_data)
  
    save_quotes(quotes)
    
    
    for quote_item in quotes:
        generate_quote_image(quote_item, bg_color, text_color)

if __name__ == "__main__":
    main()
