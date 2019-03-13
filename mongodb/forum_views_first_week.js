//getting forum views for first week, week 34, 
cursor = isye = db.ISYE6501.aggregate([
	{ $match: 
		{"name": "edx.forum.thread.viewed", 
			$expr: {$eq: 
				[{$week: 
	    			{$dateFromString: 
	    				{dateString: 
	    					{ $substr: [ "$time", 0, 10 ] }
	    				}
	    			}
	    		},
	    		34
	    		]
			} 
    	},
    },
    { $group: { _id: "$context.user_id", total: {$sum: 1}}},
    { $sort: {total: -1 } }
])
while(cursor.hasNext()){
    printjson(cursor.next());
}
