summarize_hours
===============

This is a simple script to take hours recorded in a yaml file and summarize
them several ways.

```bash
$ summarize_hours example/daily.yaml 2015-08-20 2015-08-22

                        08-20 08-21 Total
                        ----- ----- -----
proj1                 :  0.00  3.00  3.00
proj2                 :  0.00  1.00  1.00
proj3                 :  6.00  5.00 11.00
proj4                 :  1.00  0.00  1.00
proj5                 :  2.00  0.00  2.00
Total                 :  9.00  9.00 18.00

proj1
- Worked on the foozalator.
- Worked on the foozalator more.

proj2
- Worked on the splatzleblock.

proj3
- Started on the Baz feature.
- Finished the Baz feature.
- Tested the Baz feature. Fixed bug 1537.

proj4
- Phone meeting.

proj5
- Discussion with clients.
```


Discussion
----------

* Should I have used Pandas?  Probably.
* Should I have docstrings and tests?  Definitely.
