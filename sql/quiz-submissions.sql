select join1.student_item_id, join1.latest_id, join1.course_id, join1.uuid, join1.attempt_number, join1.submitted_at, join1.created_at, join1.status, edx.submissions_studentitem.item_id, edx.submissions_studentitem.item_type
from 
	(select edx.submissions_scoresummary.student_item_id, edx.submissions_scoresummary.latest_id, edx.submissions_scoresummary.course_id, edx.submissions_submission.uuid, edx.submissions_submission.attempt_number, edx.submissions_submission.submitted_at, edx.submissions_submission.created_at, edx.submissions_submission.status 
		from edx.submissions_scoresummary left join edx.submissions_submission 
		on edx.submissions_scoresummary.student_item_id=edx.submissions_submission.student_item_id) 
		as join1 
	join edx.submissions_studentitem 
	on join1.student_item_id=edx.submissions_studentitem.id 
	where edx.submissions_studentitem.course_id='course-v1:GTx+ISYE6501x+3T2018';

--Note: assessment category seems to be unused for this course?

--Rubric items are unused, for instance.
--Only a subset of classes use rubrics, and we can't make sense of Open Assessment Data w/o a rubric.

select * from edx.assessment_assessment where course_id='course-v1:GTx+ISYE6501x+3T2018';
--returns nothing

select item_id, count(id) from edx.submissions_studentitem where course_id='course-v1:GTx+ISYE6501x+3T2018' group by item_id;
--returns 30 possible item_id values. What are these? I do not yet know.

--Where can we find 