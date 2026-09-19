Source: https://docs.typesafe.ai/sdk/javascript/api/interfaces/RequestOptions
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Interface: RequestOptions

Per-call options that override client settings.

## Properties



### headers?

```ts theme={null}
optional headers?: Record<string, string>;
```

Additional headers, merged over `defaultHeaders`.

***



### retry?

```ts theme={null}
optional retry?: Partial<RetryPolicy>;
```

Retry overrides for this call; omitted fields inherit client settings.

***



### signal?

```ts theme={null}
optional signal?: AbortSignal;
```

Cancellation signal for the request and pending retries.

***



### timeout?

```ts theme={null}
optional timeout?: number;
```

Timeout per attempt in milliseconds; there is no total retry budget.
