import requests
import pandas as pd
import time

# URL del server FHIR per Ingredient e MedicinalProductDefinition
base_fhir_url = "https://jpa.unicom.datawizard.it/fhir"
# base_fhir_url = "http://localhost:3080/fhir"
ingredient_url = f"{base_fhir_url}/Ingredient"

params = {
    "_elements": "substance,for"
}

def get_all_entries(url, params=None):
    entries = []
    while url:
        try:
            response = requests.get(url, params=params)
            print(f"Status code for Ingredient request: {response.status_code}")
            data = response.json()
            entries.extend(data.get('entry', []))

            # Trova il link alla pagina successiva, se esiste
            url = None
            for link in data.get('link', []):
                if link.get('relation') == 'next':
                    url = link.get('url')
                    break
            time.sleep(1)  # Ritardo di 1 secondo tra le richieste
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta: {e}")
            time.sleep(5)  # Aspetta 5 secondi prima di ritentare
    return entries

# Eseguire la chiamata API per ottenere tutti gli Ingredient
ingredient_entries = get_all_entries(ingredient_url, params)
print(f"Totale Ingredient analizzati: {len(ingredient_entries)}")

# Estrarre le sostanze uniche e le referenze ai MedicinalProductDefinition
substances_by_country = {}

def get_medicinal_product_definition(mpd_id):
    url = f"{base_fhir_url}/MedicinalProductDefinition/{mpd_id}"
    while True:
        try:
            response = requests.get(url)
            print(f"Status code for MedicinalProductDefinition request ({mpd_id}): {response.status_code}")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta di MedicinalProductDefinition: {e}")
            time.sleep(5)  # Aspetta 5 secondi prima di ritentare

ingredient_count = 0

for entry in ingredient_entries:
    ingredient_count += 1
    resource = entry['resource']
    substance = resource.get('substance', {})

    # Estrarre sostanze da 'substance.code.concept.coding'
    code = substance.get('code', {})
    concept = code.get('concept', {})
    codings = concept.get('coding', [])

    for coding in codings:
        substance_display = coding.get('display')
        substance_code = coding.get('code')

        # Aggiungere referenze ai MedicinalProductDefinition e ottenere subito il paese
        for ref in resource.get('for', []):
            if 'MedicinalProductDefinition' in ref['reference']:
                mpd_id = ref['reference'].split('/')[-1]
                medicinal_product_data = get_medicinal_product_definition(mpd_id)
                if medicinal_product_data:
                    product_names = medicinal_product_data.get('name', [])

                    for product_name in product_names:
                        usages = product_name.get('usage', [])
                        for usage in usages:
                            country = usage.get('country', {})
                            country_codings = country.get('coding', [])

                            for country_coding in country_codings:
                                country_name = country_coding.get('display')
                                key = (country_name, substance_display, substance_code)
                                if key not in substances_by_country:
                                    substances_by_country[key] = 0
                                substances_by_country[key] += 1
                time.sleep(1)  # Ritardo di 1 secondo tra le richieste

    # Estrarre sostanze da 'substance.strength.referenceStrength.substance.concept.coding'
    strengths = substance.get('strength', [])
    for strength in strengths:
        reference_strengths = strength.get('referenceStrength', [])
        for reference_strength in reference_strengths:
            ref_substance = reference_strength.get('substance', {})
            ref_concept = ref_substance.get('concept', {})
            ref_codings = ref_concept.get('coding', [])

            for ref_coding in ref_codings:
                ref_substance_display = ref_coding.get('display')
                ref_substance_code = ref_coding.get('code')

                # Aggiungere referenze ai MedicinalProductDefinition e ottenere subito il paese
                for ref in resource.get('for', []):
                    if 'MedicinalProductDefinition' in ref['reference']:
                        mpd_id = ref['reference'].split('/')[-1]
                        medicinal_product_data = get_medicinal_product_definition(mpd_id)
                        if medicinal_product_data:
                            product_names = medicinal_product_data.get('name', [])

                            for product_name in product_names:
                                usages = product_name.get('usage', [])
                                for usage in usages:
                                    country = usage.get('country', {})
                                    country_codings = country.get('coding', [])

                                    for country_coding in country_codings:
                                        country_name = country_coding.get('display')
                                        key = (country_name, ref_substance_display, ref_substance_code)
                                        if key not in substances_by_country:
                                            substances_by_country[key] = 0
                                        substances_by_country[key] += 1
                        time.sleep(1)  # Ritardo di 1 secondo tra le richieste

    if ingredient_count % 100 == 0:
        print(f"Ingredient analizzati: {ingredient_count}")
        time.sleep(10)  # Pausa di 10 secondi ogni 100 Ingredient

# Convertire i risultati in un DataFrame per una visualizzazione più semplice
results = [(country, substance, code, count) for (country, substance, code), count in substances_by_country.items()]
df_substances_by_country = pd.DataFrame(results, columns=['Country', 'Substance', 'Code', 'Product Count'])

# Mostrare i risultati
print("Substances by Country and Product Count:")
print(df_substances_by_country)

# Salvare i risultati su file CSV
df_substances_by_country.to_csv("substances_by_country.csv", index=False)
