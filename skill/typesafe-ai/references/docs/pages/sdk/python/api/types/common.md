Source: https://docs.typesafe.ai/sdk/python/api/types/common
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Common types

> Common types for TypeSafe API SDK.

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




  typesafe\_sdk.JSONValue


`module-attribute`

<SdkSignature>
  JSONValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | Sequence["JSONValue | None"]
    | Mapping[str, "JSONValue | None"]
)

</SdkSignature>

A JSON-like value. May be nested and contain `None`.


  typesafe\_sdk.JSONContent


`module-attribute`

<SdkSignature>
  JSONContent: TypeAlias = (
    str
    | Mapping[str, JSONValue | None]
    | Sequence[JSONValue | None]
)

</SdkSignature>

Either a plain string or a mapping/sequence of [`JSONValue`](common.md#typesafe_sdk.JSONValue) entries.
