Source: https://docs.typesafe.ai/sdk/javascript/api/classes/APIUserAbortError
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Class: APIUserAbortError

The caller cancelled the request through an `AbortSignal`.

## Extends

* [`TypeSafeError`](TypeSafeError.md)

## Constructors



### Constructor

```ts theme={null}
new APIUserAbortError(message?, options?): APIUserAbortError;
```

#### Parameters

##### message?

`string` = `"Request was aborted."`

##### options?

`ErrorOptions`

#### Returns

`APIUserAbortError`

#### Overrides

[`TypeSafeError`](TypeSafeError.md).[`constructor`](TypeSafeError.md#sdk-constructor)
