
totalpinner = 0
totalkuler = 0

for n in range(1, 51):
    print(f"Antall pinner for figur {n}: {n+(n-1)}")
    print(f"Antall kuler for figur {n}: {n*(n-1)}")
    
    totalpinner += n+(n-1)
    totalkuler += n*(n-1)
    
print(f"TOTAL PINNER: {totalpinner}")
print(f"TOTAL KULER: {totalkuler}")