import heapq

heap = []
data = [(10,"ten"), (3,"three"), (5,"five"), (7,"seven"), (9, "nine"), (2,"two")]
for item in data:
    heapq.heappush(heap, item)
sorted = []
print (heap)    
while heap:
    sorted.append(heapq.heappop(heap))
print (heap)    
print (sorted)
data.sort()
print (data == sorted)