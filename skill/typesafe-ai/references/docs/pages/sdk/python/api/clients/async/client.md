Source: https://docs.typesafe.ai/sdk/python/api/clients/async/client
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Asynchronous client

> Use AsyncTypeSafeClient to ask questions, list models, and configure asynchronous TypeSafe API requests.

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




  typesafe\_sdk.AsyncTypeSafeClient


<SdkSignature>
  AsyncTypeSafeClient(
    *,
    api_key: str | None = None,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    headers: Mapping[str, str] | None = None,
    transport: httpx2.AsyncBaseTransport
    | None = None,
    http_client: httpx2.AsyncClient
    | None = None,
    base_url: str | None = None,
)

</SdkSignature>

Create an asynchronous HTTP client for [TypeSafe AI API](https://typesafe.ai).

Explicit options take precedence over environment variables; empty or whitespace-only environment values are ignored.

<Tip>
  **Logging setup**

  The SDK logs to the `typesafe_sdk` logger; configure it through standard logging, or set `TYPESAFE_LOG_LEVEL` (`debug`, `info`, ...) for a quick default. Secret headers are redacted from log output; request and response bodies are not.
</Tip>

Parameters:

* **`api_key`** (<code>str | None</code>, default: `None` ) –

  Required API key; may be set via the `TYPESAFE_API_KEY` environment variable.
* **`model`** (<code>str | None</code>, default: `None` ) –

  Model name; may be set via the `TYPESAFE_DEFAULT_MODEL` environment variable.
* **`retry`** (<code>RetryPolicy | None</code>, default: `None` ) –

  A `RetryPolicy` controlling retry behavior; see `RetryPolicy` for the available options and their defaults. Pass `RetryPolicy(max_retries=0)` to disable retries.
* **`timeout`** (<code>float | httpx2.Timeout | None</code>, default: `None` ) –

  Timeout for HTTP operations. Inherits `http_client.timeout` when supplied, otherwise the SDK default.
* **`headers`** (<code>Mapping\[str, str] | None</code>, default: `None` ) –

  Additional request headers to set.
* **`transport`** (`httpx2.AsyncBaseTransport | None`, default: `None` ) –

  Optional custom HTTP transport, closed when this SDK client closes.
* **`http_client`** (<code>httpx2.AsyncClient | None</code>, default: `None` ) –

  Optional `httpx2.AsyncClient`; mutually exclusive with `transport`. Closed when this SDK client closes.
* **`base_url`** (<code>str | None</code>, default: `None` ) –

  API root; may be set via the `TYPESAFE_BASE_URL` environment variable.

Raises:

* <code>TypeSafeError</code> –

  The API key is missing or the timeout is invalid.
* <code>ValueError</code> –

  Both `transport` and `http_client` are supplied.

Examples:

```python theme={null}
import asyncio

from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul


async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        result = await client.system_one(
            state="I was charged twice. Please help.",
            questions={
                "billing": Noul(instructions="Is this about billing?"),
                "tone": Choice(
                    instructions="What is the tone?",
                    criteria={"calm": None, "angry": None},
                ),
            },
        )
        assert 0 <= result.nouls["billing"].noul <= 1
        assert result.choices["tone"].choice in {"calm", "angry"}


asyncio.run(main())
```


  models


`cached` `property`

<SdkSignature>
  
    models
  

  
    :
  

   

  
    
      AsyncModels
    
  

  

</SdkSignature>

An accessor for the Models API resource.

Examples:

```python theme={null}
async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        models = await client.models.list()
```


  system\_one


`async`

<SdkSignature>
  system_one(
    state: JSONContent,
    questions: Mapping[str, Question],
    *,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float
    | httpx2.Timeout
    | None = None,
    extra_headers: Mapping[str, str]
    | None = None,
    extra_body: Mapping[str, JSONValue | None]
    | None = None,
) -> SystemOneResponse

</SdkSignature>

Answer named questions about text or structured state.

See [System One](../../../../../concepts/system-one.md) for details.

Parameters:

* **`state`** (<code>JSONContent</code>) –

  Text, a JSON object, or an array to evaluate. See [state](../../../../../concepts/state.md) for details.
* **`questions`** (<code>Mapping\[str, Question]</code>) –

  Nonempty mapping of names to question objects or raw dictionaries.
* **`model`** (<code>str | None</code>, default: `None` ) –

  Model override; `None` inherits the client default.
* **`retry`** (<code>RetryPolicy | None</code>, default: `None` ) –

  An optional retry policy to override the client-level value for this call only.
* **`timeout`** (<code>float | httpx2.Timeout | None</code>, default: `None` ) –

  An optional timeout for http operations to override the client-level value for this call only, in seconds.
* **`extra_headers`** (<code>Mapping\[str, str] | None</code>, default: `None` ) –

  Additional request headers to set.
* **`extra_body`** (<code>Mapping\[str, JSONValue | None] | None</code>, default: `None` ) –

  Additional top-level request-body fields, shallow-merged over the body after `state`, `model`, and `questions` are set. Merging is last-write-wins: a key that collides with `state`, `model`, or `questions` overrides it, and object values are replaced rather than deep-merged.

Returns:

* <code>SystemOneResponse</code> –

  Answers keyed by question name, with model and token usage details.

Raises:

* <code>TypeSafeError</code> –

  Questions are empty or a score question's criteria list is empty.
* <code>TypeSafeAPIError</code> –

  The server returns an unsuccessful HTTP response after any retries.
* <code>TypeSafeAPIConnectionError</code> –

  The request cannot connect or times out after any retries.

Examples:

Create questions with named arguments:

```python theme={null}
async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        result = await client.system_one(
            state="I was charged twice. Please help.",
            questions={
                "billing": Noul(instructions="Is this about billing?"),
                "tone": Choice(
                    instructions="What is the tone?",
                    criteria={"calm": None, "angry": None},
                ),
            },
        )
        assert 0 <= result.nouls["billing"].noul <= 1
        assert result.choices["tone"].choice in {"calm", "angry"}
```

Pass questions as dictionaries:

```python theme={null}
async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        result = await client.system_one(
            state={"message": "I was charged twice. Please help."},
            questions={
                "billing": {"type": "noul", "instructions": "Is this about billing?"},
                "tone": {
                    "type": "choice",
                    "instructions": "What is the tone?",
                    "criteria": {"calm": None, "angry": None},
                },
            },
        )
        assert 0 <= result.nouls["billing"].noul <= 1
        assert result.choices["tone"].choice in {"calm", "angry"}
```


  aclose


`async`

```python theme={null}
aclose() -> None
```

Release network resources and close the underlying HTTP client, including a supplied one.
