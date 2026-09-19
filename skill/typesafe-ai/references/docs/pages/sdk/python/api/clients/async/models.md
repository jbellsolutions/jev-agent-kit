Source: https://docs.typesafe.ai/sdk/python/api/clients/async/models
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Models resource

> List the models available to your account through the asynchronous client's Models resource.

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



Reached through [`AsyncTypeSafeClient.models`](client.md).


  typesafe\_sdk.AsyncModels


Access to the models available to the account, reached through `AsyncTypeSafeClient.models`.


  list


`async`

<SdkSignature>
  list(
    *,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    extra_headers: Mapping[str, str]
    | None = None,
) -> ListModelsResponse

</SdkSignature>

List the models available to the account.

Parameters:

* **`retry`** (<code>RetryPolicy | None</code>, default: `None` ) –

  An optional retry policy to override the client-level value for this call only.
* **`timeout`** (<code>float | httpx2.Timeout | None</code>, default: `None` ) –

  Per-operation timeout override; `None` inherits the client setting.
* **`extra_headers`** (<code>Mapping\[str, str] | None</code>, default: `None` ) –

  Overrides for additional request headers; authentication, SDK identification, and `Accept` remain protected.

Returns:

* <code>ListModelsResponse</code> –

  A `ListModelsResponse` whose `models` holds each model's name, description,
* <code>ListModelsResponse</code> –

  and release date.

Raises:

* <code>TypeSafeAPIError</code> –

  The server returns an unsuccessful HTTP response after any retries.
* <code>TypeSafeAPIConnectionError</code> –

  The request cannot connect or times out after any retries.

Examples:

```python theme={null}
from typesafe_sdk import AsyncTypeSafeClient


async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        models = await client.models.list()
```
