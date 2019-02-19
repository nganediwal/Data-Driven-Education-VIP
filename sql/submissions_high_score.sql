create view edx.submissions_high_score
as
select summary.course_id, 
    studentid.user_id, 
    studentitem.item_id, 
    score.points_earned, 
    score.points_possible
    score.points_earned/score.points_possible grade
from edx.submissions_score score
join edx.submissions_scoresummary summary
    on summary.highest_id = score.id
join edx.submissions_studentitem studentitem
    on studentitem.id = score.student_item_id
join edx.student_anonymoususerid studentid
    on studentid.anonymous_user_id = studentitem.student_id
order by 1;