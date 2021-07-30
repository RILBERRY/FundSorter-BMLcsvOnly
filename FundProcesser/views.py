from django.shortcuts import redirect, render
from .models import CSV_FILE
import csv
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.method == 'POST':
        Accounts = []
        Alies = []
        File = request.FILES['csv']
        UploadFile = CSV_FILE.objects.create(RawFile = File)
        UploadFile.save()


        FileData = CSV_FILE.objects.last()
        RawFile = open('Media/' + str(FileData.RawFile))
        FileData = csv.reader(RawFile)
        x = 0
        r = 0
        CurRow = 1
        try:

            for row in FileData:
                if not CurRow == 1:
                    pos = 0
                    tempTans = []
                    if row[2] == "Transfer Debit" or row[2] == "ATM Withdrawal" :
                        tempTans.append(row[0])
                        tempTans.append(row[6])
                        tempTans.append("DR")
                        tempTans.append(row[8])
                    else:
                        tempTans.append(row[0])
                        tempTans.append(row[6])
                        tempTans.append("CR")
                        tempTans.append(row[9])
                    if not row[6] in Accounts:
                        tempAlies=[]
                        Accounts.append(row[6])
                        tempAlies.append(tempTans)
                        Alies.append(tempAlies)
                    else:
                        pos = Accounts.index(row[6])
                        Alies[pos].append(tempTans)
                
                CurRow +=1

            
            # witer to csv
            response = HttpResponse(content_type = 'text/cvs')

            writer = csv.writer(response)

            Items = 0
            while Items < len(Accounts):
                writer.writerow([ Accounts[Items], "", "", ""])
                writer.writerow(['DATE', 'DES', 'DR', 'CR'])
                for Trans in Alies[Items]:
                    if Trans[2] == "DR":
                        writer.writerow([Trans[0] , Trans[1], Trans[3], 0])
                    elif Trans[2] =="CR":
                        writer.writerow([Trans[0] , Trans[1], 0, Trans[3]])

            
                Items += 1
                writer.writerow(["", "BALANCE", "", ""])
                writer.writerow(["", "", "", ""])
            response['Content-Disposition'] = 'attachment; filename="SortedFund.csv"'
   
            CurRow -= 2
            print(str(CurRow) + " Rows processed")
            return response
        except:
            return redirect('index')

    else:
        return render(request, 'index.html')


