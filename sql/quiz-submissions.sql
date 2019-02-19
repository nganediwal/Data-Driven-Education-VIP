select
    summary.student_item_id, 
    summary.latest_id, 
    summary.course_id, 
    submission.uuid, 
    submission.attempt_number, 
    submission.submitted_at, 
    submission.created_at, 
    submission.status,
    studentitem.item_id, 
    studentitem.item_type
from edx.submissions_scoresummary summary
join edx.submissions_submission submission
    on summary.student_item_id = submission.student_item_id
join edx.submissions_studentitem studentitem
    on summary.student_item_id = studentitem.id 
    and studentitem.course_id='course-v1:GTx+ISYE6501x+3T2018';

--Note: assessment category is unused for this course
--Rubric items are unused
--Only a subset of classes use rubrics, and we can't make sense of Open Assessment Data w/o a rubric.

select * from edx.assessment_assessment where course_id='course-v1:GTx+ISYE6501x+3T2018';
--returns nothing

select item_id, count(id) from edx.submissions_studentitem where course_id='course-v1:GTx+ISYE6501x+3T2018' group by item_id;
/*
These are the "problems", which are multiple choice questions. Here's an example of the raw XML for one:
<problem display_name="Question 7a" group_access="{&quot;50&quot;: [1]}" markdown="null" max_attempts="1" showanswer="past_due" weight="5.0">
  <label>What should the retailer do?</label>
  <multiplechoiceresponse>
    <choicegroup type="MultipleChoice">
      <choice correct="false">Switch to exploitation (utilize Option A only)</choice>
      <choice correct="true">Switch to exploitation (utilize Option B only)</choice>
      <choice correct="false">More exploration (testing both options more)</choice>
    </choicegroup>
  </multiplechoiceresponse>
</problem>
There is unfortunately no table with information about these, we will have to make our own if the data is valuable enough.

Note: I'm not sure what submission.status is, it's either "A" or "D" but it's not documented in the data dictionary!!!
*/

-- If you'd like to limit yourself to quiz results, use this query (in ISYE6501 only 1 submission is allowed)

select studentid.user_id, studentitem.item_id, score.points_earned, score.points_possible
from edx.submissions_score score
join edx.submissions_scoresummary summary
    on summary.highest_id = score.id
    and score.course_id = 'course-v1:GTx+ISYE6501x+3T2018'
join edx.submissions_studentitem studentitem
    on studentitem.id = score.student_item_id
join edx.student_anonymoususerid studentid
    on studentid.anonymous_user_id = studentitem.student_id
order by 1;