//getting events X weeks

var totalArray = []

var events = ["edx.forum.thread.viewed", "edx.forum.comment.created", "edx.forum.response.created"];
var weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

weeks.forEach(function(week) {
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
			    		(31 + week)
			    		]
					} 
		    	},
		    },
		    { $group: { _id: "$context.user_id", element: {$sum: 1}}},
		    { $sort: {total: -1 } }
		])
		cursorA = JSON.stringify(cursorA.toArray()).split("\"element\":").join("\"event\": \"" + element + ".week" + week + "\", \"count\":");
		totalArray = totalArray.concat(JSON.parse(cursorA))
	});
});
print("{ \"events\" : " + JSON.stringify(totalArray) + "}")
// totalArray.forEach(function(element) {
// 	printjson(element)
// });

