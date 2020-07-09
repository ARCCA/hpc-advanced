---
title: "Scheduler advice"
teaching: 20
exercises: 10
questions:
- "What possible methods are there to run my job in the scheduler?"
- "What information is available for the user?"
- "How does a scheduler allocate resource?"
objectives:
- "Understand many ways to run jobs in a scheduler."
- "Use the tools in the scheduler to find useful information."
- "Understand the decisions a scheduler has to make when allocating resource."
keypoints:
- "The scheduler can only allocate resource with the information given."
---

Much of the scheduler advice for performance can now be found in [previous training](slurm_advanced_topics).  However
general advice is

 * Job arrays are useful for repetative tasks where only the input file changes.
 * Find from SLURM how your job has performed in the scheduler with `sacct`.

For developers you can use libraries such as:
 * NetCDF for gridded data
 * Intel MKL for linear algebra problems

> ## Finding job efficiency
>
> Using `sacct` find the job efficiency for a SLURM job.
>
> > ## Solution
> > 
> > Use `sacct -j <jobid> -o "CPUTime, UserCPU"` and compare difference.
> {: .solution}
{: .challenge}

When using AMD nodes on Hawk the MKL library is setup to override the standard options and force it to use AVX2 through
setting an environment variable.  Try not to change the environment variable `MKL_DEBUG_TYPE`

Finally, please get in touch - ARCCA is here to help you are a researcher to perform you work efficiently and
effectively.

{% include links.md %}

