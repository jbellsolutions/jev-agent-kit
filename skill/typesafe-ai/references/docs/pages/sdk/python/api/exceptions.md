Source: https://docs.typesafe.ai/sdk/python/api/exceptions
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Exceptions

> Handle TypeSafe API errors, rate limits, connection failures, and timeouts.

export function SdkSignature({children}) {
  async function copy(event) {
    const button = event.currentTarget;
    const code = button.parentElement.querySelector("pre code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.setAttribute("aria-label", "Signature copied");
      button.dataset.copied = "true";
    } catch {
      button.setAttribute("aria-label", "Copy failed; select the signature to copy");
    }
    setTimeout(() => {
      button.setAttribute("aria-label", "Copy signature");
      delete button.dataset.copied;
    }, 2000);
  }
  return 
      <button type="button" className="sdk-signature-copy" aria-label="Copy signature" onClick={copy}>
        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <rect x="8" y="8" width="12" height="12" rx="2" />
          <path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3" />
        </svg>
      </button>
      <pre tabIndex={0} aria-label="SDK signature"><code>{children}</code></pre>
    ;
}




  Base exception



  typesafe\_sdk.TypeSafeError


Bases: <code>Exception</code>

Base exception for SDK failures.


  HTTP errors



  typesafe\_sdk.TypeSafeAPIError


Bases: <code>TypeSafeError</code>

An unsuccessful HTTP response with its body and request metadata.


  status


`instance-attribute`

```python theme={null}
status = status
```

HTTP response status code.


  body


`instance-attribute`

```python theme={null}
body = body
```

The server's JSON error body, plain response text, or `None` for an empty body.


  headers


`instance-attribute`

```python theme={null}
headers = headers
```

HTTP response headers.


  endpoint


`instance-attribute`

```python theme={null}
endpoint = endpoint
```

The request method and URL, without credentials, query parameters, or fragment, when available.


  request\_id


`property`

<SdkSignature>
  
    request_id
  

  
    :
  

   

  
    
      str
    
  

   

  
    |
  

   

  
    None
  

  

</SdkSignature>

The `x-typesafe-request-id` response header, or `None` if absent.


  typesafe\_sdk.TypeSafeBadRequestError


Bases: <code>TypeSafeAPIError</code>

The request was invalid (400).


  typesafe\_sdk.TypeSafeAuthenticationError


Bases: <code>TypeSafeAPIError</code>

Authentication failed (401).


  typesafe\_sdk.TypeSafePermissionDeniedError


Bases: <code>TypeSafeAPIError</code>

Access was denied (403).


  typesafe\_sdk.TypeSafeNotFoundError


Bases: <code>TypeSafeAPIError</code>

The resource was not found (404).


  typesafe\_sdk.TypeSafeUnprocessableEntityError


Bases: <code>TypeSafeAPIError</code>

The request failed server validation (422).


  typesafe\_sdk.TypeSafeRateLimitError


Bases: <code>TypeSafeAPIError</code>

The rate limit was exceeded (429).


  retry\_after\_ms


`instance-attribute`

```python theme={null}
retry_after_ms = parse_retry_after(headers)
```

The server's requested wait in milliseconds, or `None` if unavailable.


  typesafe\_sdk.TypeSafeInternalServerError


Bases: <code>TypeSafeAPIError</code>

The server failed to process the request (5xx).


  Connection errors



  typesafe\_sdk.TypeSafeAPIConnectionError


Bases: <code>TypeSafeError</code>, <code>ConnectionError</code>

A request failed without an HTTP response.


  typesafe\_sdk.TypeSafeAPITimeoutError


Bases: <code>TypeSafeAPIConnectionError</code>, <code>TimeoutError</code>

A request exceeded its configured timeout.


  timeout


`instance-attribute`

```python theme={null}
timeout = timeout
```

The timeout setting used for the request, in seconds or as an `httpx2.Timeout`.


  Response validation



  typesafe\_sdk.TypeSafeAPIResponseValidationError


Bases: <code>TypeSafeAPIError</code>

A successful HTTP response whose body was missing or structurally invalid required data.


  field\_path


`instance-attribute`

```python theme={null}
field_path = field_path
```

Dotted path to the offending field, such as `answers.tone.confidence`.


  args


`instance-attribute`

```python theme={null}
args = (
    status,
    body,
    headers,
    field_path,
    endpoint,
)
```
