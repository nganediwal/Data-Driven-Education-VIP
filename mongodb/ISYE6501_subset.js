db.edxClickStream.aggregate([ { $match: { "context.course_id": "course-v1:GTx+ISYE6501x+3T2018" } }, { $out: "ISYE6501" } ]);

