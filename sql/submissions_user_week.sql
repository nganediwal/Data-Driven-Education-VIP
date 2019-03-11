-- Selects assignment information from submissions tables (homeworks and projects)
select
    s.course_id,
    aid.user_id,
    metadata ->> 'display_name' display_name,
    (score.created_at::date - courses.start_ts::date)/7 week,
    -- extracts lead time in days
    round((
        extract(epoch from score.created_at - 
            (metadata ->> 'submission_due')::timestamp
        )/60/60/24)::numeric, 2
    ) lead_time,
    score.points_earned,
    score.points_possible,
    submission.attempt_number
from edx.submissions_studentitem s
join edx.course_structure c
    on s.item_id = c.id
    and s.course_id like '%ISYE6501x+3T2018%'
join edx.courses courses
    on courses.course_id = s.course_id
join edx.submissions_score score
    on s.id = score.student_item_id
join edx.student_anonymoususerid aid
    on s.student_id = aid.anonymous_user_id
join edx.submissions_submission submission
    on submission.id = score.submission_id
order by aid.user_id, week