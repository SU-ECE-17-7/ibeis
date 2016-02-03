'''
Introduction:  Testing IBEIS on a New Species:

This document is an iPython Notebook that summarizes a preliminary test of IBEIS on a new species.  It includes steps (a) set up and configure the IBEIS image analysis code for a new data set, (b) run the core of this code, and (c) examine the results.

To set the stage for what we are testing here, let’s jump ahead to think about how IBEIS will work once we have built a database from initial training images for a species of interest.  Given this database, IBEIS applies the following steps to each new set of images uploaded:
Gather the images taken at the same time and location (when known) to form what’s known as an occurrence.  Each image set is broken up into one or more occurrences.
Apply a detection process to each image to automatically find animals, to draw a bounding box around each, to label the species, and to determine the viewpoint on the animal.  Together, this information forms an annotation.
Within each occurrence find all annotations that are the same animal, creating what IBEIS calls an encounter.   If there are pictures of, say, five different animals in the occurrence then five encounters should be formed.   Sometimes, of course, when animals are seen individually only one encounter will be formed.
Assign a name to the animal in each encounter by matching the annotations in the encounter against the database of animals.  When this determines that an animal is previously unknown, a new name will be created and added to the database.  Information about each encounter is also added to the database.
Steps 3 and 4 are different applications of an underlying identification process whose goal is to determine which annotations show the same animal.  The success of identification is the key to the success of IBEIS’s image analysis.  Therefore, the experiments reported in this iPython notebook are designed to study how well the current identification algorithms work by simulating Step 4 of the image analysis process – the hardest step.  In addition to seeing how well the current IBEIS algorithms work, these tests can also suggest ways to improve the algorithms for the new species.

Please note that the first three sections below – with (Code) in their title -  can be safely skipped.  They were generated by the IBEIS team to run the results here.


Initialization (Code)


Pipeline Config Info (Code)


Timestamp Distribution

IBEIS will be successful if it the identification process works well when the photos of the animals are taken weeks, months or years apart.    We’d like to be able to identify an animal even if we haven’t seen it for a few years.  (Of course, even better is seeing it often.)  Therefore, the very first analysis we run on the data is to study the time distribution of the images.  The plot below shows the distribution of “Timestamps” for the images we are testing on.

Comment space below:


Example Annotations / Detections

The detection process is not shown in this iPython notebook.  This process – Step 2 in the description of the introduction – is something we usually do not apply to a new test suite of images, largely because it requires a fair amount of training data to adapt to a new species.   Shown below are example annotations.  Sometimes we have to draw them ourselves, while other times they are given to us (along with the names of the animals).

Comment space below:


Example Name Graph:

In a test where the names for each animal in each photo are provided, we can link up the annotations for each animal into what we call a name graph.    (This is done without running the IBEIS image analysis code – just from the information provided.)  We can use the name graph to spot potential problems and get an idea of how difficult the identification problem might be.   In particular, an animal whose name graph has fewer annotations will be harder to identify.  Similarly, when the name graph includes only one annotation from a particular viewpoint – such as the left flank – the animal will hard to identify if that annotation by itself was the one we tried to use to identify the animal.


Comment space below:


Query Accuracy…

Change to

Annotation Identification Accuracy:

The first and toughest test of the IBEIS identification algorithm is to take each annotation by itself and attempt to identify it.  This is done by forming a database from other the annotations in the test suite and running the identification algorithm against this database.  Other annotations from the same encounter as this “query annotation” are excluded.  This is repeated for each annotation.  This is the toughest test of image analysis because each annotation must be matched on its own, without any help from other annotations in the encounter.  So, for example, if the encounter includes annotations showing both the left and right flank of the animal, but no other annotations in the test suite show this animal’s right flank, there is no hope for success in identifying the animal from just the right flank annotation.

Results are shown below in both textual form and in a bar graph.  It is probably best to skip to the bar graph.  At this point, we should make something clear: the identification algorithm is really a ranking algorithm.  In other words, when matching the annotation, a score is generated for each named animal in the database and names (and scores) are returned ordered by the scores.  The goal is for the correct name to always be ranked first, but if it is ranked near the top it is usually ok too because the users of IBEIS make the final decisions about the identifying (and therefore naming) the animals.


 Comment space below:



Encounter Identification Accuracy:

The second test of the IBEIS identification algorithm – the most important test from the user’s perspective – is to take all the annotations in each encounter and together use them to determine the identity of the animal shown in the encounter.   Once again, this is done by forming a database from the other annotations in the test suite.   We perform this test because IBEIS algorithms combine information from matching for each annotation in an encounter to determine the final score for each possible name and thereby the final name ranking.

Identifying an animal using all the annotations in an encounter almost always improves the scoring and ranking results.  This is one reason why we strongly encourage users of the system to take and contribute several different images of each animal they encounter and not try to choose the “best” to contribute!   This simplifies the user’s job and makes the IBEIS software as effective as possible.


Comment space below:

[ Note:  could add some viewpoint analysis here!? ]


Examples of Top Scoring Successes:

The next four sections including this one show examples of Annotation Identifications that are successes (top ranked) and failures (not top ranked).  In each case results are shown in rows of two side-by-side blocks of annotations.  Each block includes two, three or four annotations.  In a block the left or upper left is the “query annotation”, i.e. the one IBEIS is trying to identify.  This annotation has a purple border around it.  Next to it and (when there are four annotations) below it are shown a set of “other” database annotations.   When the identification is correct, these other annotations are all from the same name as the query annotation.  These are framed in green.  When the identified name is incorrect these other database annotations – all from the incorrect name - are framed in red.

For the top scoring successes, we show strong true positives in the block on the left and the next best scoring true negative in the block on the right.  Two rows of blocks are shown for each result, with the top row showing just the two blocks of annotations, and the blocks in the bottom row show the annotations together with matching regions linked by a line segment between annotations.  The links go from the query annotation to the database annotations.  Usually the links are to multiple database annotations (for the same animal) since information from more than one annotation is used to make decisions.   Showing these matches allows us to understand what the image analysis algorithm used to score the match.

(Notice that sometimes you will see matches between the background regions of the annotations.  These will be eliminated in the production version of IBEIS for because IBEIS learns to figure out and ignore the background through training examples.)


Comment space below:


Examples of Challenging Successes:

This section shows Annotation Identification test cases where the top scoring name is correct, but the score is low and close to the score of the next best matching name.


Comment space below:


Examples of High-Scoring Failures:

This section shows Annotation Identification test examples where the correct name is not the top scoring matching, but it scored reasonably high.  In each case, the annotations from the incorrect matching name are shown in the block on the left (along with the query annotation), while annotations from the correct matching name are shown in the block on the right.


Comment space below:



Examples of Low-Scoring Failures:

This section shows Annotation Identification test examples where the correct name is not the top scoring match, and the correct name scored quite poorly.  In each case, the annotations from the incorrect matching name are shown in the block on the left (along with the query annotation), while annotations from the failed but correct matching name are shown in the block on the right.  Such failures are most often due to low quality annotations, occlusions, or the query annotation showing a view of the animal that is not in any annotation in the database.


Comment space below:



[ For each of the remaining sections add (Details, Safely Ignored) to the title ]
'''
