Source: https://docs.typesafe.ai/sdk/javascript/api/classes/APITimeoutError
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Class: APITimeoutError

The full response did not arrive within the timeout. A kind of `APIConnectionError`.

## Extends

* [`APIConnectionError`](APIConnectionError.md)

## Constructors



### Constructor

```ts theme={null}
new APITimeoutError(timeoutMs, options?): APITimeoutError;
```

#### Parameters

##### timeoutMs

`number`

##### options?

`ErrorOptions`

#### Returns

`APITimeoutError`

#### Overrides

[`APIConnectionError`](APIConnectionError.md).[`constructor`](APIConnectionError.md#sdk-constructor)

## Properties



### timeoutMs

```ts theme={null}
readonly timeoutMs: number;
```

Configured timeout in milliseconds.
