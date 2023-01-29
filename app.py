from flask import Flask, jsonify, redirect, request
from PyPDF2 import PdfReader
import re
import json
from string import digits


app = Flask(__name__)

@app.route("/extract-data", methods=['POST'])
def extractData(): 
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    filename = file.filename
    reader = PdfReader(filename)
    page = reader.pages[0]
    text = page.extract_text()
    Stops = [i for a,i in enumerate(re.search(r"((.*(\n|\r|\r\n)){21})Truck Information:", text).group().splitlines()[2:-1]) if i!=' ']
    res = {
        "data": {
            "RateconKeystone": {
                "CustomerName": {
                    "Address1": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][1],
                    "Address2": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][2],
                    "BillingInfo": {
                        "Address1": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][1],
                        "Address2": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][2],
                        "City": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[0],
                        "Email": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "Fax": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "Name": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][0],
                        "Phone": re.search(r"Phone:\s+\d+.\d+.\d+", text).group()[7:],
                        "PhoneExt": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "State": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[1:],
                        "Zip": re.sub("[^0-9]", "",re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3])
                    },
                    "City": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[0],
                    "ContactPerson/Dispatcher": re.search(r"Dispatcher:\s+\w+", text).group().split(':')[1][1:],
                    "ContactPersonPhone": re.search(r"Phone:\s+\d+.\d+.\d+", text).group()[7:],
                    "DispatcherEmail": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "Email": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "Fax": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "Name": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][0],
                    "Notes": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "PaymentTerms": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "Phone": re.search(r"Phone:\s+\d+.\d+.\d+", text).group()[7:],
                    "PhoneExt": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "QuickPayPCT": re.search(r"Pieces:\s+\d+", text).group()[8:],
                    "State": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[1:],
                    "TrackerEmail": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                    "Zip": re.sub("[^0-9]", "",re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3])
                },
                "EquipmentName": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                "IsHazmat": re.search(r"Pieces:\s+\d+", text).group()[8:],
                "LoadAmount": re.sub("[^0-9]", "",re.search(r"Total Pay:\s+.\d+.\d+", text).group()),
                "LoadCategory": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                "LoadType": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                "Miles": re.sub("[^0-9]", "",re.search(r"(Total.*)miles", text).group()),
                "Notes": re.sub(' +', ' ',re.search(r"Notes\s+pu.*\s*del.*", text).group().replace("\n"," ")[6:]),
                "PowerOnlyLoad": re.search(r"Pieces:\s+\d+", text).group()[8:],
                "RateDetails": [
                    {
                        "Amount": re.search(r"((.*(\n|\r|\r\n)){4})Please sign", text).group().splitlines()[:-1][1][10:],
                        "DescriptionName": re.search(r"((.*(\n|\r|\r\n)){4})Please sign", text).group().splitlines()[:-1][1][:8],
                        "PER": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "Units": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1]
                    },
                    {
                        "Amount": re.search(r"((.*(\n|\r|\r\n)){4})Please sign", text).group().splitlines()[:-1][2][4:],
                        "DescriptionName": re.search(r"((.*(\n|\r|\r\n)){4})Please sign", text).group().splitlines()[:-1][2][:3],
                        "PER": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "Units": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1]
                    },
                    {
                        "Amount": re.search(r"((.*(\n|\r|\r\n)){4})Please sign", text).group().splitlines()[:-1][3][16:],
                        "DescriptionName": re.search(r"((.*(\n|\r|\r\n)){4})Please sign", text).group().splitlines()[:-1][3][:14],
                        "PER": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "Units": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1]
                    }
                ],
                "RefNumber": re.sub("[^0-9]", "",re.search(r"Load.*", text).group()),
                "Stops": [
                    {
                        "Address1": Stops[1],
                        "Address2": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "AppNumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "City": Stops[2].split(',')[0],
                        "Contact": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "FCFS": re.search(r"Pieces:\s+\d+", text).group()[8:],
                        "FacilityName": Stops[0],
                        "FromDate": re.search("[0-9]+\/[0-9]+\/[0-9]+",Stops[7]).group(),
                        "FromTime": re.search("[0-9]+\:[0-9]+\:[A-Z]+",Stops[7]).group(),
                        "IsAppRequired": re.search(r"Pieces:\s+\d+", text).group()[8:],
                        "Notes": "pick " + re.search("((.*(\n|\r|\r\n)){2})del#",text).group().splitlines()[1].split('pick')[1],
                        "Special Instructions": Stops[5] +" "+ Stops[6],
                        "PONumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1], 
                        "Phone": Stops[3].split(': ')[1],
                        "ReturnTrailer": re.search(r"Pieces:\s+\d+", text).group()[8:],
                        "SealNumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],      
                        "State": Stops[2].split(',')[1].translate(str.maketrans('', '', digits))[1:],
                        "StopItems": [
                            {
                                "CONumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Commodity": re.search(r"Commodity#\s.\s\w+\s\w+", text).group().split(': ')[1],
                                "ItemNumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Length": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "PONumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1], 
                                "Pallets": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "PieceCount": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Weight": re.search(r"Weight#\s:\s\d+", text).group().split(': ')[1]
                            }
                        ],
                        "StopNumber": 1,
                        "StopType": "Pickup",
                        "Temperature": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "ToDate": re.search("[0-9]+\/[0-9]+\/[0-9]+",Stops[7]).group(),
                        "ToTime": re.search("[0-9]+\:[0-9]+\:[A-Z]+",Stops[7]).group(),
                        "Zip": re.sub("[^0-9]", "", Stops[2])
                    },
                    {
                        "Address1": Stops[9],
                        "Address2": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "AppNumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "City": Stops[10].split(',')[0],
                        "Contact": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "FCFS": re.search(r"Pieces:\s+\d+", text).group()[8:],
                        "FacilityName": Stops[8],
                        "FromDate": re.search("[0-9]+\/[0-9]+\/[0-9]+",Stops[14]).group(),
                        "FromTime": re.search("[0-9]+\:[0-9]+\:[A-Z]+",Stops[14]).group(),
                        "IsAppRequired": re.search(r"Pieces:\s+\d+", text).group()[8:],
                        "Notes": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "Special Instructions": Stops[13],
                        "PONumber": re.search(r"Notes\s+pu#\s\w+\s+\w+", text).group().replace("\n",""),
                        "Phone": Stops[11].split(': ')[1],
                        "ReturnTrailer": re.search(r"Pieces:\s+\d+", text).group()[8:],
                        "SealNumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "State": Stops[10].split(',')[1].translate(str.maketrans('', '', digits))[1:],
                        "StopItems": [
                            {
                                "CONumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Commodity": re.search(r"Commodity#\s.\s\w+\s\w+", text).group().split(': ')[1],
                                "ItemNumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Length": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "PONumber": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Pallets": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "PieceCount": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                                "Weight": re.search(r"Weight#\s:\s\d+", text).group().split(': ')[1]
                            }
                        ],
                        "StopNumber": 2,
                        "StopType": "Drop",
                        "Temperature": re.search(r"((.*(\n|\r|\r\n)){5})Notes", text).group().splitlines()[:-2][3].split(',')[1].translate(str.maketrans('', '', digits))[:1],
                        "ToDate": re.search("[0-9]+\/[0-9]+\/[0-9]+",Stops[14]).group(),
                        "ToTime": re.search("[0-9]+\:[0-9]+\:[A-Z]+",Stops[14]).group(),
                        "Zip": re.sub("[^0-9]", "", Stops[10])
                    }
                ],
                "Temperature": re.search("((.*(\n|\r|\r\n)){2})del#",text).group().splitlines()[1].split('**** ')[1].split('F ')[0] + " F"
            }
        },
        "message": "Files successfully!"
    }

    with open(f'{filename[:-4]}.json', 'w') as fp:
        json.dump(res, fp)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
