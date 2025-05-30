import requests
import pandas as pd

chemical_cas_numbers = {
    'BENTAZON': '25057-89-0',
    'PENOXSULAM': '219714-96-2',
    'PERMETHRIN': '52645-53-1',
    'ENDOSULFAN': '115-29-7',
    'GLYPHOSATE': '1071-83-6',
    'HEXAHYDRO-1,3,5-TRINITRO-1,3,5-TRIAZINE': '121-82-4',  # RDX
    '2-AMINO-4,6-DINITROTOLUENE': '35572-78-2',
    'HEXAHYDRO-1-NITROSO-3,5-DINITRO-1,3,5-TRIAZINE': '5755-27-1',  # MNX
    'HEXAHYDRO-1,3,5-TRINITROSO-1,3,5-TRIAZINE': '13980-04-6',  # TNX
    'CARBARYL': '63-25-2',
    'CHLORPYRIFOS': '2921-88-2',
    'TOXAPHENE (POLYCHLORINATED CAMPHENES)': '8001-35-2',
    'ENDRIN': '72-20-8',
    'DIELDRIN': '60-57-1',
    'MEXACARBATE': '315-18-4',
    'EPN': '2104-64-5',
    'FENTHION': '55-38-9',
    'CARBOFURAN': '1563-66-2',
    'MONOCROTOPHOS': '6923-22-4',
    'AZINPHOS-METHYL (GUTHION)': '86-50-0',
    'TRIFLUOROMETHYL-4-NITROPHENOL (3-, LAMPRECIDE)': '88-30-2',
    'SODIUM  MONOFLUOROACETATE': '62-74-8',
    'STRYCHNINE': '57-24-9',
    'ZINC PHOSPHIDE': '1314-84-7',
    "DDT (4,4'-)": '50-29-3',
    'METHYLPARATHION': '298-00-0',
    'AMINOPYRIDINE (4-)': '504-24-5',
    'ALDICARB': '116-06-3',
    'CYANIDE, SODIUM': '143-33-9',
    'PARA-AMINOPROPIOPHENONE': '70-69-9',
    'DIPHACINONE': '82-66-6',
    'ALDRIN': '309-00-2',
    'LINDANE': '58-89-9',
    'DICROTOPHOS': '141-66-2',
    'DIURON': '330-54-1',
    'PROPOXUR': '114-26-1',
    'FENSULFOTHION': '115-90-2',
    'DEMETON': '8065-48-3',
    'MERCURIC CHLORIDE': '7487-94-7',
    'AMMONIUM NITRATE': '6484-52-2',
    'AMMONIUM CHLORIDE': '12125-02-9',
    'AMMONIUM SULFATE': '7783-20-2',
    'NITRATE, SODIUM': '7631-99-4',
    'TETRACHLORODIBENZO-P-DIOXIN (2,3,7,8-)': '1746-01-6',  # TCDD
    "PCB 126 (3,3',4,4',5-PENTACHLOROBIPHENYL)": '57465-28-8',
    'PHOSPHORUS (YELLOW OR WHITE)': '7723-14-0',
    'EMAMECTIN BENZOATE': '155569-91-8',
    'PARATHION': '56-38-2',
    'FORMALDEHYDE': '50-00-0',
    'ZINC SULFATE': '7733-02-0',
    'COPPER SULFATE': '7758-98-7',
    '2,4,6-TRINITROTOLUENE': '118-96-7',  # TNT
    'LEAD ACETATE': '301-04-2',
    '2,4-DINITROTOLUENE': '121-14-2',
    'METHYLMERCURY': '22967-92-6',
    'THEOBROMINE': '83-67-0'
}

headers = {
    "Accept": "application/json"
}

chem_headers = ['ChemicalName', 'MolecularWeight', 'XLogP', 'TPSA', 'HBondDonorCount', 'HBondAcceptorCount']
chem_df = pd.DataFrame(columns=chem_headers)
for chem in chemical_cas_numbers:
    print(chem, ": ", chemical_cas_numbers[chem])
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_cas_numbers[chem]}/property/MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount/JSON"
    response = requests.get(url, timeout=10)
    data = response.json()
    props = data['PropertyTable']['Properties'][0]
    row = {
        'ChemicalName': chem,
        'MolecularWeight': props.get('MolecularWeight'),
        'XLogP': props.get('XLogP'),
        'TPSA': props.get('TPSA'),
        'HBondDonorCount': props.get('HBondDonorCount'),
        'HBondAcceptorCount': props.get('HBondAcceptorCount'),
    }
    chem_df.loc[len(chem_df)] = row

chem_df.to_csv('../Data/ChemicalData.csv')
