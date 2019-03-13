cursor = isye = db.ISYE6501.aggregate([
	{ $match: {"name": "edx.forum.thread.viewed" }},
    { $group: 
    	{ _id: 
    		{$subtract:
	    		[ {$week: 
	    			{$dateFromString: 
	    				{dateString: 
	    					{ $substr: [ "$time", 0, 10 ] }
	    				}
	    			}
	    		},
	    		34
	    		]	
    		}, 
		total: { $sum: 1 } } },
    { $sort: {total: -1 } }
])
while(cursor.hasNext()){
    printjson(cursor.next());
}