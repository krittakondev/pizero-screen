import cups

def get_printed_and_requested_pages():
    conn = cups.Connection()
    jobs = conn.getJobs(my_jobs=True, requested_attributes=['job-media-sheets-completed', 'job-k-octets'])
    total_pages_printed = 0
    total_pages_requested = 0

    print(jobs)
    for job_id, job in jobs.items():
        if 'job-media-sheets-completed' in job:
            total_pages_printed += job['job-media-sheets-completed']
        if 'job-k-octets' in job:
            # Estimate number of pages based on job size in kilobytes
            # This is a rough estimate, you might need more precise calculation based on specific printer/job attributes
            total_pages_requested += job['job-k-octets'] // 1024

    return total_pages_printed, total_pages_requested

total_pages_printed, total_pages_requested = get_printed_and_requested_pages()
print(f"Total pages printed: {total_pages_printed}")
print(f"Total pages requested: {total_pages_requested}")

