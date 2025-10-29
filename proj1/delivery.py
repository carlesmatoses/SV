import zipfile

with zipfile.ZipFile('carles-matoses.zip', 'w') as z:
    z.write('country_lists_enriched.csv', arcname='carles-matoses/country_lists_enriched.csv')
    z.write('reportv2.ipynb', arcname='carles-matoses/carles-matoses.ipynb')
    z.write('app.py', arcname='carles-matoses/carles-matoses.py')