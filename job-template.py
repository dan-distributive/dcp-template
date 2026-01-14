#  File:        template-job.py
#  Description: Template job demonstrating most options; serves as a tutorial and is extensible
#
#  Author:      Dan Desjardins
#  Created:     2026-01-11
#  License:     MIT

#-----------------------
# DCP MODULE & INIT
#-----------------------
import dcp
dcp.init()


#-----------------------
# ID AND PAYMENT KEYS
# If this block is omitted, DCP looks in ~/.dcp for id.keystore and default.keystore.
#-----------------------

# Import DCP wallet (see wallet API: docs.dcp.dev/api/wallet/index.html)
from dcp import wallet

# Set an ID key: jobs will be owned and manageable with this key.
# wallet.get(<name>) looks in ~/.dcp for <name>.keystore
id = wallet.get("id").js_ref
dcp.identity.set(id)

# Add a payment key: compute credits will be withdrawn from this account to pay for jobs.
# For absolute paths, include the .keystore extension
pay = wallet.get("/Users/dandesjardins/.dcp/default.keystore").js_ref
wallet.add(pay)


#-----------------------
# INPUT SET
# Any iterable of items (numbers, images, data blobs, etc.)
#-----------------------
my_inps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


#-----------------------
# WORK FUNCTION
# Computationally expensive function applied to each input element
#-----------------------
def my_func(x, a, b):
    dcp.progress()                      # report indeterminate progress, see docs.dcp.dev/api/compute/functions/progress.html#progress
    
    import numpy as np                  # modules used inside work function must be imported inside work function
    from scipy.special import ive       # same requirement
    import my_module_1                  # same
    from my_modules import my_module_2  # same

    dcp.progress(0.5)                   # progress call reporting slice is 50% complete

    print("This is a worker console message and it says 'I love DCP'")
    result = np.sqrt(x) + ive(1, a) * my_module_1.some_function(b) + my_module_2.some_other_function(b)

    dcp.progress(1)                   # progress call reporting slice is 100% complete

    return result


#-----------------------
# WORK ARGUMENTS
# Static arguments for each job slice, in the same order as the work function
# arguments, except the first one which comes from the input set
#-----------------------
my_args = [
    0.1248734,     # a in my_func
    0.9876122      # b in my_func
]


#-----------------------
# DCP Job
# dcp.compute_for applies the `work_function` with the `work_arguments` to each element in the `input_set`
#-----------------------
my_job = dcp.compute_for(my_inps, my_func, my_args)


#-----------------------
# PUBLIC JOB INFO
#-----------------------
# optional and publicly-visible job info provided by the author
my_job.public = {
    "name":         "Template job",
    "description":  "DCP job with maximum options for demonstration purposes",
    "link":         "https://distributive.network",
}


#-----------------------
# COMPUTE GROUPS
# If `computeGroups` is not specified, the job runs on the Global Network.
# `computeGroups` is a list of objects of the form:
#   {"joinKey": "<key>", "joinSecret": "<secret>"}
# Instead of hardcoding secrets, this example prompts for them at deployment time.
#-----------------------

# Compute Group join keys only
my_job.computeGroups = [
    {"joinKey": "tensparrows"}
]

# Prompt for join secrets at deployment time
from getpass import getpass
for g in my_job.computeGroups:
    if g.get("joinKey") != "public":
        g["joinSecret"] = getpass(f"Enter join secret for compute group '{g['joinKey']}': ")


#-----------------------
# MODULES FROM PACKAGE MANAGER
# Specify Python modules to be fetched from the DCP package manager and
# initialized on workers at runtime. Only modules available in Pyodide
# may be used here (see: pyodide.org/en/stable/usage/packages-in-pyodide.html).
#-----------------------
my_job.modules = ["numpy", "scipy"]


#-----------------------
# FILE SYSTEM
# Specify files or directories to upload and make available to workers at runtime
#-----------------------
my_job.fs.add("./my_module_1.py")    # add a specific file
my_job.fs.add("./my_modules")        # add a directory (contains my_module_2 and sub_modules)

#-----------------------
# EVENT LISTENERS
# Register handlers for job lifecycle, progress, and result events
#-----------------------

# Timestamp helper used by event handlers
from datetime import datetime
def timestamp() -> str:
    return datetime.now().strftime("%-I:%M:%S %p")


# event: READYSTATECHANGE
def on_readystatechange(rst):
    ts = timestamp()

    print(
        f"[{ts}] [readystatechange] "
        f"{rst}"
        "\n"
    )

my_job.on('readystatechange', on_readystatechange)


# event: ACCEPTED
def on_accepted(_):
    ts = timestamp()
    job_id = my_job.id

    print(
        f"[{ts}] [accepted] "
        f"Job ID: {job_id}. Awaiting results..."
        "\n"
    )

my_job.on('accepted', on_accepted)


# event: NOPROGRESS
def on_noProgress(nop):
    ts = timestamp()
    job_id = nop['job']
    job_name = nop['jobName']
    slice_number = int(nop['sliceNumber'])
    last_progress = nop['progressReports']['last']['progress']
    message = nop['message']

    print(
        f"[{ts}] [noprogress_{slice_number}] "
        f"{message} Last progress: {last_progress}%"
        "\n"
    )

my_job.on('noProgress', on_noProgress)


# event: ERROR
def on_error(err):
    ts = timestamp()
    job_id = err['job']
    job_name = err['jobName']
    slice_number = int(err['sliceNumber'])
    message = err['message']

    print(
        f"[{ts}] [error_{slice_number}] "
        f"{message}"
        "\n"
    )

my_job.on('error', on_error)


# event: NOFUNDS
def on_nofunds(nof):
    ts = timestamp()
    job_id = nof['job']
    job_name = nof['name']
    bank_account = nof['bankAccount']
    funds_required = nof['fundsRequired']
    remaining_slices = int(nof['remainingSlices'])
    slice_payment_amount = nof['slicePaymentAmount']

    print(
        f"[{ts}] [nofunds] "
        f"Bank account {bank_account} balance below ⊇{slice_payment_amount}. {remaining_slices} slices remain, ⊇{funds_required} required to complete."
        "\n"
    )

my_job.on('nofunds', on_nofunds)


# event: RESULT
def on_result(res):
    ts = timestamp()
    job_id = res['job']
    slice_number = int(res['sliceNumber'])
    result = res['result']

    print(
        f"[{ts}] [result_{slice_number}] "
        f"{result}"
        "\n"
    )

my_job.on('result', on_result)


# event: CONSOLE
def on_console(con):
    ts = timestamp()
    job_id = con['job']
    slice_number = int(con['sliceNumber'])
    message = con['message']  # console output is a list of strings

    print(
        f"[{ts}] [console_{slice_number}] "
        f"{message}"
        "\n"
    )

my_job.on('console', on_console)


#-----------------------
# JOB DEPLOYMENT
#-----------------------
# marketValue corresponds to a per-slice price offer (in Compute Credits) calculated 
# at the current market rate, which fluctuates with supply and demand on the DCP platform.
marketValue = dcp.compute.marketValue().js_ref

# job.exec() deploys the job. With no arguments, it uses the current market rate per slice.
# You can override this by specifying a slice price offer (e.g., job.exec(123.456) = 123.456 Compute Credits per slice).
# Bidding above market accelerates execution by attracting more compute; underbidding reduces priority and slows completion.
my_job.exec(marketValue)

# On completion, my_results contains results in the same order as the input set.
# You can also use the results event to append each result to a file as it arrives.
my_results = my_job.wait()


#-----------------------
# RESULT POST-PROCESSING
#-----------------------
print(my_results)