import cups

def get_total_pages_printed():
    conn = cups.Connection()
    jobs = conn.getJobs(my_jobs=True, requested_attributes=['job-media-sheets-completed'])
    total_pages = 0

    for job_id, job in jobs.items():
        if 'job-media-sheets-completed' in job:
            total_pages += job['job-media-sheets-completed']

    return total_pages

total_pages_printed = get_total_pages_printed()
print(f"Total pages printed: {total_pages_printed}")


