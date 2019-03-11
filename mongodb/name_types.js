cursor = isye = db.ISYE6501.aggregate([
    { $group: { _id: "$name", total: { $sum: 1 } } },
    { $sort: {total: -1 } }
])
while(cursor.hasNext()){
    printjson(cursor.next());
}