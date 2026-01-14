# DCP Python Job template
Template job demonstrating most options; serves as a tutorial and is extensible.

* Main job script (`template-job.py`)
* Modules and Submodules
* Browser or Standalone [DCP Workers](https://distributive.network/)

This example shows the full end-to-end workflow with most options shown for an event-driven distributed job. Input data flows from the client to workers through the scheduler, and results flow back through the scheduler to the client. For direct worker data access that bypasses the scheduler, see remote jobs: https://github.com/dan-distributive/dcp-remote

This is a minimal Python DCP job, serving as a **starting point**. The more fully featured version with additional configuration options is in `template-job.py`:
```
import dcp
dcp.init()

def work_function(x, a, b):
    progress()
    return x * a + b

job = dcp.compute_for([1, 2, 3, 4, 5], work_function, [31, 87])
job.exec()
results = job.wait()
```

## Overview

This repository is a tutorial, not a production system. The code emphasizes clarity and is meant to be modified. Configuration and events can be adapted or promoted to command-line prompts for advanced or secure use cases.
If you encounter any issues or have questions, you can reach the team via:

* Email: info@distributive.network
* Slack: [DCP Developers Slack](https://join.slack.com/t/dcp-devs/shared_invite/zt-56v87qj7-fkqZOXFUls8rNzO4mxHaIA)

## Requirements

* Node.js
* Python
* pip packages:
  * dcp
* DCP keystore files in the home directory:
```
~/.dcp/id.keystore
~/.dcp/default.keystore
```
To obtain keystore files, contact: dan@dcp.dev

## Running the Example

**1. Launch the job:**
```
python3 template-job.py
```
You should see output similar to:
```
dandesjardins@Mac ~ % python3 DCP/DCP-tutorials/python/dcp-template/job-template.py
Enter join secret for compute group 'tensparrows': 
[11:42:25 PM] [readystatechange] exec
[11:42:25 PM] [readystatechange] init
[11:42:25 PM] [readystatechange] preauth
[11:42:25 PM] [readystatechange] deploying
[11:42:26 PM] [readystatechange] listeners
[11:42:26 PM] [readystatechange] compute-groups
[11:42:26 PM] [readystatechange] uploading
[11:42:27 PM] [readystatechange] deployed
[11:42:27 PM] [accepted] Job ID: jW4XjGOi6VEkSUlL3J1NdG. Awaiting results...
```

**2. Launch workers**

Here are 3 of the many different types of workers that can be launched:

**Docker Worker**

Documentation: [distributive.network/docs/worker-docker.pdf](https://distributive.network/docs/worker-docker.pdf)

Launch the worker with your account and compute group credentials:
```
docker run -it \
  --earnings-account=<account> \
  --no-global \
  --join <key>,<secret> \
```
* Replace `<account>` with your DCP earnings account number.
* Replace `<key>,<secret>` with your compute group join key and join secret.

**Linux Worker**

Documentation: [distributive.network/docs/worker-linux.pdf](https://distributive.network/docs/worker-linux.pdf)

If the worker is already installed, launch it with:
```
sudo --user=dcp /opt/dcp/bin/dcp-worker.sh \
  --earnings-account=<account> \
  --no-global \
  --join <key>,<secret> \
```
The same credential requirements apply as with the Docker worker.

**Browser worker**

Documentation: [distributive.network/docs/worker-browser.pdf](https://distributive.network/docs/worker-browser.pdf)

Open the following URL, replacing `key` with your compute group join key:
```
https://dcp.work/key
```
Enter the join secret when prompted.

Press `Start`


**3. Receive results:**

In your job client terminal, you should see something like:

```
...
[11:48:12 PM] [result_4] 10.030439053580421
[11:48:12 PM] [console_8] ["This is a worker console message and it says 'I love DCP'"]
[11:48:12 PM] [result_6] 10.4799287963636
[11:48:12 PM] [result_5] 10.266507031080211
[11:48:13 PM] [result_7] 10.676190364645013
[11:48:13 PM] [result_8] 10.858866178326611
[11:48:15 PM] [console_9] ["This is a worker console message and it says 'I love DCP'"]
[11:48:15 PM] [console_10] ["This is a worker console message and it says 'I love DCP'"]
[11:48:15 PM] [result_9] 11.030439053580421
[11:48:15 PM] [result_10] 11.192716713748801

[9.030439053580421, 9.444652615953517, 9.762489861149298, 10.030439053580421, 10.266507031080211, 10.4799287963636, 10.676190364645013, 10.858866178326611, 11.030439053580421, 11.192716713748801]
```


## Project Structure
```
.
├── template-job.py               # Main job script
├── my_module_1.py                # some module
└── my_modules/                   # some module directory
    └── __init__.py
    └── my_module_2.py            # another module
    └── sub_modules/              # another submodule directory
        └── __init__.py
        └── my_module_3.py        # another submodule
```


## Configuration
The following parameters can be modified:

| Parameter        | Location            | Description                                        |
| ---------------- | ------------------- | -------------------------------------------------- |
| computeGroups    | `job.computeGroups` | Set join key and join secret                       |
| name, description, and link | `job.public` | Publicly viwable information about your job    |
|slicePaymentOffer | `job.exec`          | How many compute credits offered per job slice     |
| id keystore      | `wallet.get`        | Specify which keystore file to use as identity     |
| account keystore | `wallet.get`        | Specify which keystore file to use to pay for job  |


## Extending the Example

This example shows many of the availble events and configuration to facilitate extensibility

The pattern remains:

```
job = compute_for(input_set, work_function, arguments)
job.exec()
results = job.wait()
```

*Happy computing*
