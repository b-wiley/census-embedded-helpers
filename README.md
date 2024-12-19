# Helpful functions to get off the ground when implementing Census Embedded

Census Embedded is an API driven version of Census: https://www.getcensus.com/embedded

Scripts in this repo:
- `create_sync.py`: This script creates a new sync programmatically using the existing source & destination connections in a given client's workspace.
- `new_customer_tenant.py`: This gives Census Embedded customers the ability to quickly spin up a new tenant/workspace for their clients without having to do a bunch of manual work.
- `sync_run_statuses.py`: This gives Census Embedded customers the ability to quickly implement some logic that prints & returns information about recent sync runs.
