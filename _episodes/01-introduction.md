---
title: "Introduction"
teaching: 10
exercises: 5
questions:
- "Why would I want to advance my skills?"
objectives:
- "Be able to help yourselves and others."
keypoints:
- "Advanced skills allow you to help yourself more."
---

Once you have a job running on HPC it might be tempting to stop learning further about HPC. This might be due to
resource constraints, lifespan of project, or a global pandemic.   The goal of a researcher when using HPC resource
may be to get the results, understand them and publish.  The researcher has not seen the possibility of using the HPC
resource in an efficient way that could speed up turnaround of jobs, perform quicker analysis, or fix any problems quickly
that may appear.

A researcher that can spend more time learning about HPC can perform more effectively and may see new ways to approach a
problem.

> ## What problems have you already experienced?
>
> Think about any problems you experienced, did you solve them yourself? If not, did you spend time searching for help?
> Could you have performed your work in a different (more efficient) way?  How long did your jobs run on the system?
> How did you estimate the resources required?
{: .challenge }

# Development practice on HPC

## Navigating command line and editor.

Learning to use tools correctly and effortless allows more time spend on the actual work.  Learning to drive requires
commitment and time to make the car seem to be an extension of the body.  HPC is no different, learning to use development tools to write SLURM jobs, develop
code, and managing change should be an extension of your mind without having to think about it.

HPC is a bit different to development on your desktop.  HPC tends to be run across an ssh connection so graphical
windows can be unnatural to the experience.  Software tend to be built specially for the system rather than using
generic packages from distributions that are find for a few hours use on a desktop but using it for 1000s of hours on a
HPC system requires optimisation to make use of the resource.

Due to the importance of the results coming from HPC (you do *NOT* want to rerun a jobs that can take a long time or
cost money) revision control is important. No more:

~~~
cp my_job.sh my_job_050720.sh
# edit my_job.sh
sbatch my_job.sh
# gives my_job.sh to colleague that finds error>
~~~
{: .language-bash}

And instead use Git

~~~
git clone https://github.com/ARCCA/my_job
# edit my_job.sh
sbatch my_job.sh
git add my_job.sh
git commit -m "Modified command line argument to random.exe"
git push origin
# share repository with colleague who can see changes.
~~~
{: .language-bash}

## Experiment with software

As a user on HPC you are free to build software and experiment with build options or dependencies of the software.
Doing this yourself you learn about the different options available when building software and may find more effective
set of options.  This speeds up your workflow rather than waiting for others to build the software.

# Debugging and optimisation

When you experience a problem with running a job on a HPC system or run the job in parallel to gather more results the best person to solve this is the person who
understands what is being achieved.  By giving you tools to try and find out why the job does not work will allow the
user to see and understand their job in more detail and how it impacts their work.  Of course, support is always
available where issues can be fixed but gaining the tools and knowledge should make the user feel confident about the
jobs they are running.  GPUs, filesystems, number of processors/cores to use are all important factors to understand
their uses.

> ## What are GPUs?
> Part of this workshop will look at GPUs, but what are they?  Can they be easily be used or are they specialist
> hardware?  Find out whether the software you want to run on HPC can use GPUs, it usually leads to a faster way to run
> your job.  Machine learning is the current trend to use GPUs extensively due to its natural fit to be used with GPUs.
{: .challenge}

# General knowledge of the job scheduler

Job schedulers have 1 job and that is to find the resource you request and run your job.  Job schedulers can also
provide you with different ways to run your job, maybe you need interactive session, or you need to run your job
thousands of times at the same time.  A job scheduler also records lots of information about your jobs and this can be
queried to find out more about a particular run.

Finally, when using the job scheduler SLURM do not underestimate the power of

~~~
$ man sbatch
~~~
{: .language-bash}

The `man` pages provide a wealth of information.

{% include links.md %}

