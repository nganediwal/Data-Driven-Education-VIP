//getting forum views for first week, week 34, 

var totalArray = []

var events = ["edx.forum.thread.viewed", "edx.forum.comment.created", "edx.forum.response.created"];

events.forEach(function(element) {
	cursorA = isye = db.ISYE6501.aggregate([
		{ $match: 
			{"event_type": element, 
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
	    { $group: { _id: "$context.user_id", element: {$sum: 1}}},
	    { $sort: {total: -1 } }
	])
	cursorA = JSON.stringify(cursorA.toArray()).split("\"element\":").join("\"" + element + "\":");
	totalArray = totalArray.concat(JSON.parse(cursorA))
});
print("{ \"events\" : " + JSON.stringify(totalArray) + "}")
// totalArray.forEach(function(element) {
// 	printjson(element)
// });

