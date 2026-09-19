Source: https://docs.typesafe.ai/sdk/javascript/api/classes/APIConnectionError
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Class: APIConnectionError

The request or response-body delivery failed (DNS, TLS, connection closed, etc.).

## Extends

* [`TypeSafeError`](TypeSafeError.md)

## Extended by

* [`APITimeoutError`](APITimeoutError.md)

## Constructors



### Constructor

```ts theme={null}
new APIConnectionError(message?, options?): APIConnectionError;
```

#### Parameters

##### message?

`string` = `"Connection error."`

##### options?

`ErrorOptions`

#### Returns

`APIConnectionError`

#### Overrides

[`TypeSafeError`](TypeSafeError.md).[`constructor`](TypeSafeError.md#sdk-constructor)
