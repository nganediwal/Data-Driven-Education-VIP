-- All of the combinations of cohorts and learner categories
select ce.mode, cm.name, count(*)
from edx.course_groups_cohortmembership cm
right join edx.student_courseenrollment ce
	on ce.course_id = cm.course_id
	and ce.user_id = cm.user_id
group by ce.mode, cm.name;

-- A standard table that edX should provide...
create view edx.student_type
as
-- Selecting Auditors
select ce.course_id, ce.user_id, ce.mode, cm.name, 'Audit' learner_type
from edx.course_groups_cohortmembership cm
right join edx.student_courseenrollment ce
	on ce.course_id = cm.course_id
	and ce.user_id = cm.user_id
where ce.mode = 'audit'
	and (
		cm.name like 'Audit%'
		or cm.name like 'Default%'
		or cm.name is null)
union
-- Selecting GT degree seeking students
select ce.course_id, ce.user_id, ce.mode, cm.name, 'GT' learner_type
from edx.course_groups_cohortmembership cm
right join edx.student_courseenrollment ce
	on ce.course_id = cm.course_id
	and ce.user_id = cm.user_id
where ce.mode = 'audit'
	and (
		cm.name not like 'Audit%'
		and cm.name not like 'Default%'
		and cm.name is not null)
union
-- Selecting MicroMasters students
select ce.course_id, ce.user_id, ce.mode, cm.name, 'MM' learner_type
from edx.course_groups_cohortmembership cm
right join edx.student_courseenrollment ce
	on ce.course_id = cm.course_id
	and ce.user_id = cm.user_id
where ce.mode = 'verified';