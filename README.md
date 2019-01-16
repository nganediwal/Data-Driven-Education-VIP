# Subteam Description

The majority of educational research, even just 10 years ago, was done within single classrooms, single semesters, often with thirty students or less. What could be asked was limited as well. If the researcher was lucky they would collect data from surveys and interviews, with standardized pre, mid, and post-tests. Lectures, discussions, individual assignments, even attendance would not be recorded or considered in research.

This has changed with the introduction of big data. Accredited courses are now being offered online, where thousands of students take the same course, and billions of interactions are recorded. There is a new subfield called learning analytics which is focused on the analysis of these vast datasets. I suspect that we will look back on this change as we look back on the invention of the telescope for astronomy, and the invention of the transistor for computer science.

The mission of this sub-team is to engage with learning analytics research and using Georgia Tech's unique dataset, to propel the field forward. Georgia Tech offered the first online masters degree (in computer science) beginning in 2015, and has since expanded to include a masters in analytics and now a masters in cybersecurity. This is a unique data-set as most learning analytics research is done on single undergraduate level courses.

This semester will be focused on replicating the analysis of [Gardner and Brooks, 2018](https://learning-analytics.info/journals/index.php/JLA/article/view/5814). They identified three broad categories of data used for predicting student success: clickstream, forum, and assignment data. After transforming these data into a data-frame, they trained a slew of models, with another slew of hyper-parameters. This results in a three dimensional matrix of data categories, models, and hyper-parameters. To determine what model is the "best" model, they used a Bayesian hierarchical method, which has several advantages over traditional null hypothesis significance tests (or, as was most often done in the past, no statistical model evaluation).

We are also interested in using natural language processing (NLP) to better understand forum data. An intriguing study from Georgia State, [Crossley et al., 2017](https://repository.isls.org/bitstream/1/220/1/17.pdf), determined the relative importance of forum contributions using cohesion network analysis. They found that students who posted high quality forum posts performed significantly better than students who didn't. This is at odds with other studies, such as [Gardner and Brooks, 2018](https://learning-analytics.info/journals/index.php/JLA/article/view/5814), who find that forum activity does not influence student success much at all. This difference could be due to the rudimentary treatment of forum data in Gardner and Brooks, or it could be due to the over-representation of forum data in Crossley et al. Regardless of the differences between the two studies, we would like to start using NLP and possibly cohesion network analysis with our forum data.

Once our student success models are ready, we plan to use them along with interventions that are built into Georgia Tech MOOCs. A few examples of research projects that successfully created interventions are in the reading list below. The goals of the interventions are to help students, and also to answer research questions. A few examples are in the reading list below for these interventions. This isn't the focus this semester, but keep it in mind and note any ideas you may have for interventions.

# Spring 2019 Deliverables
* Identify data to be used in student success modeling
* Clean data and bring it into a data-frame which can be used to train models
* Train models
* Evaluate models using Bayesian hierarchical methods
* Viability study for cohesion network analysis from [Crossley et al., 2017](https://repository.isls.org/bitstream/1/220/1/17.pdf)

# Team Roles and Responsibilities
* **Project Manager** Coordinate tasks between team members, keep project tasks up to date, lead presentations
* **Researcher** Read papers and identify potential intervention projects
* **Data Scientist** Write scripts to process data, train models, and evaluate results (can coordinate with integration team)
* **Web Developer** Build interventions into edX

# Reading List
## Predicting Student Success
* [Gardner and Brooks, 2018: Model Evaluation Method](https://learning-analytics.info/journals/index.php/JLA/article/view/5814)
**All sub-team members must read this paper!**
* [Crossley et al., 2017: Cohesion Network Analysis](https://repository.isls.org/bitstream/1/220/1/17.pdf)
* [O'Connell
 et al., 2018: Long Term Prediction](https://learning-analytics.info/journals/index.php/JLA/article/view/5833)

## Interventions
* [Davis et al., 2018: Retrieval Practice](https://learning-analytics.info/journals/index.php/JLA/article/view/6098)
* [Kizilcec et al., 2017: Social Identity Threat ](http://science.sciencemag.org/content/sci/355/6322/251.full.pdf)

# Researchers to Read
* [Gardner](https://scholar.google.com/citations?user=SSq1t_YAAAAJ&hl=en&oi=ao)
* [Kizilcec](https://scholar.google.com/citations?user=l3ZT5GkAAAAJ)
* [Joyner](https://scholar.google.com/citations?user=yaCigtkAAAAJ&hl=en)
