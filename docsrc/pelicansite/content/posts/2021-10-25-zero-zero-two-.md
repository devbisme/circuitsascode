Title: New Release - 0.0.2
Date: 2021-10-25
Author: Dave Vandenbout
Slug: zero-zero-two
Tags:

Well, two months after my first release comes the second.
This one adds an R-2R DAC and an adjustable voltage regulator.

Not much, you say? I agree. But other things were happening.
While doing the R-2R DAC, I discovered a problem with how SKiDL handled interfaces.
(That's one of the reasons I started circuitsascode: to help me test and debug SKiDL.)
Correcting that bug caused another problem to appear with packages and I had to fix *that*.
If that wasn't enough, I decided to move the SKiDL blog from the Jekyll static-site generator to Pelican
and then finally get the Sphinx documentation properly formatted.

In addition, I re-wrote the new and existing circuit modules to make it easier
for a user to modify the circuits that get generated.
I'll discuss how circuitsascode modules are structured in a separate post.

So not a lot appears to have happened, but progress continues under the surface.
