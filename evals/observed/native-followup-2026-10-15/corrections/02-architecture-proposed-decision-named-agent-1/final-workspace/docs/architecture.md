# Current boundary
Transport validates HTTP structure and calls application.submit_order. Business authorization and order idempotency apply to HTTP and scheduled-import callers. Storage exposes atomic insert-if-key-absent. Traffic is 5 requests/second; no accepted operational need for a new service.
